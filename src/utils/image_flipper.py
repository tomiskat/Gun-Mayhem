import pygame


class ImageFlipper:
    """
    Class for lipping images and caching them.
    """
    _cache = {}

    @classmethod
    def flip(cls, image, flip_x, flip_y):
        key = (id(image), flip_x, flip_y)

        if key in cls._cache:
            return cls._cache[key]

        flipped = pygame.transform.flip(image, flip_x, flip_y)
        cls._cache[key] = flipped
        return flipped