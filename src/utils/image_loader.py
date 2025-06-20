import glob
import os
import pygame

from typing import List, Dict


class ImageLoader:
    """
    Class for loading images. Supports loading single images from a path and
    loading all images from a folder.
    """

    _image_cache: Dict[str, pygame.Surface] = {}
    _folder_cache: Dict[str, List[pygame.Surface]] = {}

    @classmethod
    def load_image(cls, path: str) -> pygame.Surface:
        """Load a single image from a path and cache it."""
        if path in cls._image_cache:
            return cls._image_cache[path]

        image = pygame.image.load(path).convert_alpha()
        cls._image_cache[path] = image
        return image

    @classmethod
    def load_images(cls, folder: str) -> List[pygame.Surface]:
        """Load all PNG images from a folder and cache them as a list."""
        if folder in cls._folder_cache:
            return cls._folder_cache[folder]

        files = sorted(glob.glob(os.path.join(folder, "*.png")))
        images = [cls.load_image(file) for file in files]
        cls._folder_cache[folder] = images
        return images
