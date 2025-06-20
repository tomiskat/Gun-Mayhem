import os
import random
import pygame

from src.constants import colors
from src.constants.fonts import SMALL_FONT
from src.enums.entity_states import EntityState
from src.model.entity_config import EntityConfig
from src.utils.image_flipper import ImageFlipper
from src.utils.image_loader import ImageLoader
from src.utils.image_scaler import ImageScaler
from src.weapons.weapon_factory import WeaponFactory


class Entity(pygame.sprite.Sprite):
    """
    Base class for all entities in the game.
    """

    def __init__(self, config: EntityConfig, image_path: str):
        super().__init__()
        self.map_data = config.map_data
        self.entity_data = config.entity_data
        self.physics = config.physics
        self.image_path = image_path

        self._load_entity_attributes()
        self._load_weapon(config.on_bullet_created)
        self._load_animations()
        self._create_sprite_image()
        self._initialize_state()
        self._reset_position()

    def _load_entity_attributes(self):
        """
        Load basic attributes like name, lives, and size.
        """
        self.name = self.entity_data["name"]
        self.lives = self.entity_data["lives"]
        self.width = self.map_data.width // 20
        self.height = self.map_data.height // 10
        self.name_space = self.map_data.height // 70
        self.bullet_size = (2 * self.height // 4, self.height // 4)

    def _initialize_state(self):
        """
        Initialize entity movement, state, and animation-related attributes.
        Called also when the entity respawns.
        """
        self.facing_right = random.choice([True, False])
        self.vx = self.vy = self.knockback_x = 0
        self.frame_index = 0.0
        self.shooting = False
        self.on_ground = False
        self.skip_platform = False
        self.platform = 0
        self.state = EntityState.IDLE

    def _reset_position(self):
        """
        Randomize the initial x-position of the entity within a central spawn range.
        Ensures the entity spawns within 25% to 175% of the map's horizontal midpoint.
        """
        spawn_center = (self.map_data.width - self.width) // 2
        spawn_multiplier = random.uniform(0.25, 1.75)
        spawn_x = int(spawn_center * spawn_multiplier)
        self.rect = self.image.get_rect(topleft=(spawn_x, 0))

    def _create_sprite_image(self):
        """
        Create the sprite image. This image is used by pygame group to detect collisions.
        It is also used to draw the entity on the screen - however we use custom draw methods.
        """
        self.image = self.state_animations[EntityState.IDLE][0]

    def _load_animations(self):
        self._load_static_animations()
        self._load_shooting_animations()

    def _load_static_animations(self):
        """
        Load animations for each state with scaled sizes and flipped versions.
        """
        self.state_animations, self.flipped_state_animations = {}, {}
        for state in EntityState:
            path = os.path.join(self.image_path, state.name.lower())
            normal, flipped = self._load_scaled_images(path, self.width, self.height)
            self.state_animations[state] = normal
            self.flipped_state_animations[state] = flipped

    def _load_shooting_animations(self):
        """
        Loading shooting animations. Scaled to 1.5 times the entity's width because
        shooting images are wider than state images.
        """
        path = os.path.join(self.image_path, 'shooting')
        animations = self._load_scaled_images(path, int(1.5 * self.width), self.height)
        self.shooting_animations, self.flipped_shooting_animations = animations

    def _can_land(self, tile: pygame.Rect) -> bool:
        """
        Determine if entity can land on the given tile considering platform skipping.
        If skip platform is set to True, the entity can only land on the platform below
        the current one.
        """
        if not self._tile_collision(tile, self.rect):
            return False
        if self.skip_platform and tile.top == self.platform:
            return False

        self._tile_collision(tile, self.rect)
        return True

    def _apply_gravity(self):
        self.vy += self.physics.gravity

    def _relax_knockback(self):
        """
        Gradually relax knockback effect caused by being hit by bullet.
        """
        self.knockback_x *= self.physics.knockback_decay
        if abs(self.knockback_x) < self.physics.knockback_decay:
            self.knockback_x = 0

    def _move_and_collide(self):
        """
        Move entity horizontally and vertically based on velocity and knockback.
        Check for landing on platforms or falling off map.
        """
        self.rect.x += self.vx + self.knockback_x
        self.rect.y += self.vy

        if self.vy > 0:
            self.on_ground = False
            self._check_landing()
            self._check_fall_off_map()

    def _get_tiles_in_column(self):
        """
        Get all the tiles in the map column the entity is in.
        """
        mid_x = self.rect.centerx
        col_index = int((mid_x / self.map_data.width) * self.map_data.cols)
        tiles = self.map_data.platforms.get(col_index, [])
        return tiles

    def _check_landing(self):
        """
        Check if the entity collides with a platform. If so, check if
        the entity is landing on the platform.
        """
        for tile in self._get_tiles_in_column():
            if self._can_land(tile):
                self.rect.y = tile.top - self.height
                self.vy = 0
                self.on_ground = True
                self.platform = tile.top
                self.skip_platform = False
                return

    def _check_fall_off_map(self):
        """
        In case the entity falls off the map, reset its state and position. If the entity
        has no lives left, kill it. Killing the entity will remove ti from pygame sprites
        group and entity will no longer be updated or drawn.
        """
        if self.rect.y > self.map_data.height:
            self._initialize_state()
            self._reset_position()
            self.lives -= 1
            if self.lives <= 0:
                self.kill()

    def _is_platform_before(self) -> bool:
        """
        Check if the entity is on a platform. If so, check if there is a platform
        in the direction the entity is facing.
        """
        if not self.on_ground:
            return False

        direction = 1 if self.facing_right else -1
        next_x = self.rect.centerx + direction * self.rect.width / 2
        col_index = int((next_x / self.map_data.width) * self.map_data.cols)
        tiles = self.map_data.platforms.get(col_index, [])

        for tile in tiles:
            if tile.top == self.platform:
                return True
        return False

    def _is_platform_below(self) -> bool:
        tiles = self._get_tiles_in_column()
        return len(tiles) > 0 and tiles[-1].top > self.rect.bottom

    def _is_jumpable_platform_above(self) -> bool:
        tiles = self._get_tiles_in_column()
        for i, tile in enumerate(tiles):
            if tile.top == self.platform and i >= 1:
                tile_above = tiles[i - 1]
                return tile_above.top >= self.rect.bottom + self.physics.jump_height

        return False

    def _set_state(self, state: EntityState):
        if self.state != state:
            self.state = state
            self.frame_index = 0.0


    def _draw_standard(self, surface):
        """
        Draw the entity on the surface. Used for all animations except shooting.
        """
        animations = self.state_animations if self.facing_right else self.flipped_state_animations
        images = animations[self.state]
        surface.blit(images[int(self.frame_index)], self.rect.topleft)
        self.frame_index = (self.frame_index + self.physics.animation_speed) % len(images)


    def _draw_shooting(self, surface):
        """
        Draw shooting animation. As the shooting images are wider than state images,
        we need to offset the shooting images to the left or right depending on the
        direction the entity is facing to let the animation look natural.
        """
        animations = self.shooting_animations if self.facing_right else self.flipped_shooting_animations
        image = animations[int(self.frame_index)]
        offset = 0 if self.facing_right else -int(self.width * 0.5)
        surface.blit(image, (self.rect.x + offset, self.rect.y))
        self._update_shooting_animation()

    def _update_shooting_animation(self):
        """
        Update shooting animation. When the animation reaches the last frame, stop the
        animation and reset the frame index to 0 also change shooting state to false.
        """
        self.frame_index += self.physics.animation_speed
        if int(self.frame_index) >= len(self.shooting_animations):
            self.shooting = False
            self.frame_index = 0.0

    def _draw_name(self, surface):
        """
        Draw entity’s name just above the sprite
        """
        name = SMALL_FONT.render(self.name, True, colors.WHITE)
        name_rect = name.get_rect(center=(self.rect.centerx, self.rect.y - self.name_space))
        surface.blit(name, name_rect)

    def _shoot(self):
        """
        Shoot if not already shooting. Define the position of the bullet.
        Cooldowns for individual weapons could be added later.
        """
        if not self.shooting:
            self.shooting = True
            self.frame_index = 0.0
            x_pos = self.rect.right if self.facing_right else self.rect.left
            y_pos = (self.rect.top + self.rect.centery) // 2
            self.weapon.shoot((x_pos, y_pos), self.facing_right)

    def _load_weapon(self, on_bullet_created):
        """
        Load the weapon of the entity based on the weapon name defined in the JSON file. Also
        passing callable on_bullet_created. We use it to specify into which pygame group the
        bullet should be added (player bullets or enemy bullets).
        """
        bullet_path = os.path.join(self.image_path, "bullet.png")
        bullet_img = ImageScaler.scale_image(ImageLoader.load_image(bullet_path), *self.bullet_size)
        self.weapon = WeaponFactory.get_weapon(
            weapon_name=self.entity_data["weapon"],
            on_bullet_created=on_bullet_created,
            bullet_images=[bullet_img, ImageFlipper.flip(bullet_img, True, False)],
            bullet_speed=self.physics.bullet_speed,
            bullet_damage=self.physics.bullet_damage
        )

    def update(self, *args, **kwargs):
        """
        The methods that are executed in each frame.
        """
        super().update(*args, **kwargs)
        self._apply_gravity()
        self._move_and_collide()
        self._relax_knockback()
        self._update_state()

    def draw(self, surface: pygame.Surface):
        """
        Draw entity name and the entity itself.

        We use custom draw method because when entity is shooting, its images have different sizes
        than the state images, and we would have to change self.image that is used by pygame group
        to draw sprites.
        """
        self._draw_name(surface)
        self._draw_shooting(surface) if self.shooting else self._draw_standard(surface)

    def _update_state(self):
        """
        Update the state of the entity based on its velocity. We do not differentiate all possible
        states of the entity. For example, when the entity is falling, its state is IDLE. The states
        purpose is to decide which animation to be drawn. If the entity is shooting, we do not
        change its state because the shooting animations are different.
        """
        if self.shooting:
            return

        if self.vy < 0:
            self._set_state(EntityState.JUMPING)
        elif self.vx == 0:
            self._set_state(EntityState.IDLE)
        else:
            self._set_state(EntityState.RUNNING)

    @staticmethod
    def _tile_collision(tile: pygame.Rect, rect: pygame.Rect):
        """
        Check if the entity collides with a tile.
        """
        return tile.top <= rect.bottom <= tile.centery

    @staticmethod
    def _load_scaled_images(path: str, width: int, height: int):
        """
        Load all images from path, scale them, and create flipped versions
        """
        images = ImageLoader.load_images(path)
        scaled = [ImageScaler.scale_image(img, width, height) for img in images]
        flipped = [ImageFlipper.flip(img, True, False) for img in scaled]
        return scaled, flipped
