from typing import Tuple

import pygame

from src.constants.fonts import SMALL_FONT
from src.utils.image_scaler import ImageScaler
from src.constants import colors


class EntityPanel:
    """
    A UI panel displaying an entity's image, name, and dynamic lives count.
    """
    def __init__(self, size: Tuple[int, int], position: Tuple[int, int], spacing: int,
                 entity_name: str, entity_image: pygame.Surface):
        self.width, self.height = size
        self.x, self.y = position
        self.spacing = spacing
        self.surface = pygame.Surface(size, pygame.SRCALPHA)
        self._create_image(entity_image)
        self._create_panel_text(entity_name)


    def _create_image(self, entity_image):
        """
        Create an image from the given entity image by scaling it to fit the panel.
        """
        img_max_w = self.width // 3 - self.spacing
        img_max_h = self.height - self.spacing
        iw, ih = entity_image.get_size()
        scale = min(img_max_w / iw, img_max_h / ih)
        self.scaled_image = ImageScaler.scale_image(entity_image, int(iw * scale), int(ih * scale))

    def _create_panel_text(self, name):
        """
        Prepares static name text and computes layout for dynamic lives text. Please beware
        that this method requires the scaled image of the entity, therefore it has to be
        called after _create_image() method.
        """
        self.name_text = SMALL_FONT.render(name, True, colors.BLACK)
        self.lives_text_color = colors.LIVES_PLAYER if name == "Player" else colors.LIVES_ENEMY

        dummy_lives_text = SMALL_FONT.render("Lives: 0", True, self.lives_text_color)
        image_width = self.scaled_image.get_width()
        available_width = self.width - image_width

        self.name_text_x = image_width + (available_width - self.name_text.get_width()) // 2
        self.lives_text_x = image_width + (available_width - dummy_lives_text.get_width()) // 2
        self.text_y = (self.height - self.name_text.get_height() - dummy_lives_text.get_height() - self.spacing) // 2


    def draw(self, surface, lives):
        """
        Draw the panel. Needs to be called in each frame, because when entity dies, it is respawned
        at the top of screen and can redraw the panel.
        """
        self._draw_background()
        self._draw_panel_image()
        self._draw_panel_text(lives)
        surface.blit(self.surface, (self.x, self.y))

    def _draw_background(self):
        """
        Draw white panels with a black border.
        """
        rect = pygame.Rect(0, 0, self.width, self.height)
        pygame.draw.rect(self.surface, colors.WHITE, rect, border_radius=10)
        pygame.draw.rect(self.surface, colors.BLACK, rect, 2, border_radius=10)

    def _draw_panel_image(self):
        """
        Draw the entity image.
        """
        self.surface.blit(self.scaled_image, (self.spacing // 2, self.spacing // 2))

    def _draw_panel_text(self, lives):
        """
        Draw the panel text with entity name and lives count.
        """
        lives_text = SMALL_FONT.render(f"Lives: {lives}", True, self.lives_text_color)
        self.surface.blit(self.name_text, (self.name_text_x, self.text_y))
        self.surface.blit(lives_text, (self.lives_text_x, self.text_y + self.name_text.get_height() + self.spacing))
