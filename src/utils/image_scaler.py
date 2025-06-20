from typing import Dict, Tuple

import pygame

class ImageScaler:
    """
    Scale an image to a given width and height.
    """

    _cache: Dict[Tuple[int, int, int], pygame.Surface] = {}

    @classmethod
    def scale_image(cls, image: pygame.Surface, width: int, height: int) -> pygame.Surface:
        key = (id(image), width, height)
        if key in cls._cache:
            return cls._cache[key]

        scaled_image = pygame.transform.smoothscale(image, (width, height))
        cls._cache[key] = scaled_image
        return scaled_image
