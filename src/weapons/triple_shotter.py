from typing import Callable, Tuple

import pygame

from src.weapons.bullet import Bullet
from src.weapons.weapon import Weapon


class TripleShotter(Weapon):
    """
    A special weapon that fires three bullets simultaneously in a vertical column.
    """

    def __init__(self, on_bullet_created: Callable[[Bullet], None], bullet_images: list[pygame.Surface],
                 bullet_speed: float, bullet_damage: float) -> None:
        super().__init__(on_bullet_created, bullet_images, bullet_speed, bullet_damage)

    def shoot(self, position: Tuple[int, int], facing_right: bool) -> None:
        bullet_height = self.bullet_images[0].get_height()
        offsets = [-2 * bullet_height, 0, 2 * bullet_height]

        for offset in offsets:
            bullet_position = (position[0], position[1] + offset)
            super().shoot(bullet_position, facing_right)
