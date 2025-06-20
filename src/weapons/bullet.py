import pygame

from typing import Tuple

class Bullet(pygame.sprite.Sprite):
    """
    Bullet class to represent a projectile fired by a weapon. The damage is initial number
    of pixels by which the entity is knocked back (summed to current knockback and entity
    moving speed). The damage effect is relaxed in each frame until it reaches 0.
    """
    def __init__(self, position: Tuple[int, int], speed: float, damage: float, image: pygame.Surface):
        super().__init__()
        self.speed = speed
        self.damage = damage
        self.image = image
        self.rect = (self.image.get_rect(center=position))

    def update(self, map_width: int) -> None:
        """
        Update bullet position. And destroy bullet if it goes off the map.
        """
        self.rect.x += self.speed
        if self._is_off_map(map_width):
            self.kill()

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.image, self.rect)

    def _is_off_map(self, map_width: int) -> bool:
        return self.rect.right < 0 or self.rect.left > map_width



