import os
import pygame

from pygame.key import ScancodeWrapper
from src.constants.paths import IMAGE_PATH
from src.entities.entity import Entity
from src.model.entity_config import EntityConfig


class Player(Entity):
    def __init__(self, entity_config: EntityConfig):
        image_path = os.path.join(IMAGE_PATH, 'entity', 'player')
        super().__init__(entity_config, image_path)
        self._create_vision_rect()
        self.rect.center = 383, 320

    def _create_vision_rect(self):
        """
        Create a rectangle of same size as the player sprite.
        It is used to detect upcoming collisions with bullets.
        """
        self.vision_rect = self.rect.copy()
        self.vision_rect.topleft = (self.rect.x, self.rect.y)
        self.vision_rect.center = self.rect.center

    def update(self, *args, **kwargs):
        """
        Same as parent method, but also handles player keystrokes.
        """
        self._handle_input()
        super().update(*args, **kwargs)

    def _handle_input(self):
        keys = pygame.key.get_pressed()
        self._process_horizontal_input(keys)
        self._process_vertical_input(keys)
        self._process_shooting_input(keys)

    def _process_horizontal_input(self, keys: ScancodeWrapper):
        """
        Move the player horizontally if the left or right key is pressed.
        If the player is already shooting, only moving to the side on which
        the player is facing is allowed.
        """
        self.vx = 0

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            if not (self.shooting and self.facing_right):
                self.vx = -self.physics.move_speed
                self.facing_right = False

        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            if not (self.shooting and not self.facing_right):
                self.vx = self.physics.move_speed
                self.facing_right = True

    def _process_vertical_input(self, keys: ScancodeWrapper):
        """
        Handle the player jumping and platform skipping. If the player
        is not on the ground, he can't jump or skip a platform.
        """
        if not self.on_ground:
            return

        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            if self._is_platform_below():
                self.on_ground = False
                self.skip_platform = True

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.on_ground = False
            self.vy = self.physics.jump_speed

    def _process_shooting_input(self, keys: ScancodeWrapper):
        if keys[pygame.K_SPACE] or keys[pygame.K_p]:
            self._shoot()


