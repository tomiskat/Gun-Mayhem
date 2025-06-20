import os.path
import pygame

from src.constants.paths import IMAGE_PATH
from src.entities.entity import Entity
from src.model.entity_config import EntityConfig


class Enemy(Entity):
    def __init__(self, entity_config: EntityConfig):
        image_path = os.path.join(IMAGE_PATH, 'entity', 'enemy')
        super().__init__(entity_config, image_path)
        self._init_vision_sprite()

    def _init_vision_sprite(self):
        """
        Create a vision sprite to detect incoming bullets. The range is based on
        bullet speed, jump strength and sprite size.
        """
        self._vision_range = abs(self.physics.bullet_speed * self.physics.jump_speed) - self.width // 2
        self._vision_sprite = pygame.sprite.Sprite()
        self._vision_sprite.rect = pygame.Rect(self.rect.x, self.rect.y, self.width, self.height)

    def update(self, *args, **kwargs):
        self._ai_logic(
            player_bullets=kwargs.get('player_bullets'),
            player_center=kwargs.get('player_center'),
            player_platform=kwargs.get('player_platform')
        )
        super().update(*args, **kwargs)

    def _ai_logic(self, player_bullets, player_center, player_platform):
        """
        Simple AI logic:
        - Move toward the player’s platform
        - Face the player
        - Shoot and dodge player bullets
        - Stay near platform center
        """
        if self.platform != player_platform:
            self._navigate_to_platform(player_platform)
        else:
            self._face_player(player_center)
            #self._shoot()
            self._dodge_bullets(player_bullets)
            self._move_to_map_center()

    def _face_player(self, player_center):
        """
        Turn to face the player if not shooting.
        """
        if not self.shooting:
            self.facing_right = player_center >= self.rect.centerx

    def _dodge_bullets(self, bullets: pygame.sprite.Group):
        """
        Check for bullets within the vision range and jump if needed. To make AI more unfathomable
        we could also consider skipping platforms.
        """
        offset = self._vision_range if self.facing_right else -self._vision_range
        self._vision_sprite.rect.topleft = (self.rect.x + offset, self.rect.y)

        if pygame.sprite.spritecollide(self._vision_sprite, bullets, dokill=False):
            if self.on_ground:
                self.on_ground = False
                self.vy = self.physics.jump_speed

    def _navigate_to_platform(self, target_platform):
        """
        Decide whether to move up or down to reach the target platform.
        """
        if self.on_ground:
            self._move_down() if self.platform < target_platform else self._move_up()


    def _move_down(self):
        """
        Move down to a lower platform by skipping current platform, if possible. Otherwise,
        move horizontally if not already moving.
        """
        if self._is_platform_below():
            self.vx = 0
            self.on_ground = False
            self.skip_platform = True
        else:
            self._move_if_idle()

    def _move_up(self):
        """
        Jump to a higher platform if possible. Otherwise, move horizontally
        if not already moving.
        """
        if self._is_jumpable_platform_above():
            self.vx = 0
            self.on_ground = False
            self.vy = self.physics.jump_speed
        else:
            self._move_if_idle()

    def _move_if_idle(self):
        """
        Move horizontally if not already moving. Choose such a direction that the sprite
        will be moving to the horizontal center of the map.
        """
        if self.vx == 0:
            self.facing_right = self.rect.centerx <= self.map_data.width // 2
            self.vx = self.physics.move_speed if self.facing_right else -self.physics.move_speed

    def _move_to_map_center(self):
        """
        Move horizontally toward the center of the map if far enough and currently facing
        in the correct direction (to disable moving backwards). The facing direction is
        based on player position.
        """
        self.vx = 0
        if self._is_platform_before():
            map_center_x = self.map_data.width // 2
            distance = self.rect.centerx - map_center_x
            tolerance = self.width // 2

            if abs(distance) > tolerance:
                if distance < 0 and self.facing_right:
                    self.vx = self.physics.move_speed
                elif distance > 0 and not self.facing_right:
                    self.vx = -self.physics.move_speed
