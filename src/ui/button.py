import pygame
from typing import Tuple
from src.constants import colors
from src.constants.fonts import MEDIUM_FONT


class Button:
    """
    Helper ui component to create clickable buttons.
    """
    def __init__(self, rect: pygame.Rect, on_click: callable):
        self.rect = rect
        self.on_click = on_click

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.on_click()

    def draw(self, surface: pygame.Surface, text: str, color: Tuple[int, int, int], text_color=colors.WHITE):
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        text = MEDIUM_FONT.render(text, True, text_color)
        text_rect = text.get_rect(center=self.rect.center)
        surface.blit(text, text_rect)