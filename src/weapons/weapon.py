from typing import Callable, Tuple

import pygame

from src.weapons.bullet import Bullet

class Weapon:
    """
    Base class for all weapons. Contains bullet creation logic and method for shooting. THe bullet
    images is a tuple of two images, one for each buller direction (right and left).
    """
    def __init__(self, on_bullet_created: Callable[[Bullet], None], bullet_images: list[pygame.Surface],
                 bullet_speed: float, bullet_damage: float) -> None:
        self.on_bullet_created = on_bullet_created
        self.bullet_images = bullet_images
        self.bullet_speed = bullet_speed
        self.bullet_damage = bullet_damage

    def shoot(self, position: Tuple[int, int], facing_right: bool) -> None:
        """
        Fire a bullet based on the given position and facing direction. The on_bullet_created
        callback adds the bullet to the bullet group (player or enemy).
        """
        if facing_right:
            speed = self.bullet_speed
            damage = self.bullet_damage
            image = self.bullet_images[0]
        else:
            speed = -self.bullet_speed
            damage = -self.bullet_damage
            image = self.bullet_images[1]

        bullet = Bullet(position, speed, damage, image)
        self.on_bullet_created(bullet)


