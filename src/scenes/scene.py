import pygame

from src.constants import colors
from src.constants.paths import BACKGROUND
from src.managers.game_manager import GameManager
from src.utils.image_loader import ImageLoader
from src.utils.image_scaler import ImageScaler


class Scene:
    """
    Base class for game scenes. It draws a base surface each time when game is switched to
    another scene.
    """

    def __init__(self, surface: pygame.Surface, game_manager: GameManager):
        self.surface = surface
        self.game_manager = game_manager
        self.width, self.height = surface.get_size()
        self.background = self._load_scaled_background()

    def _load_scaled_background(self) -> pygame.Surface:
        image = ImageLoader.load_image(BACKGROUND)
        return ImageScaler.scale_image(image, self.width, self.height)

    def initialize(self):
        """Create base background surface."""
        self.surface.fill(colors.BLACK)
        self.surface.blit(self.background, (0, 0))

    def draw(self):
        """
        Override to implement custom drawing. Beware that pygame group method draw()
        does not call this method.
        """
        pass

    def handle_event(self, event: pygame.event.Event):
        """Override to handle input events."""
        pass

    def update(self):
        """Override for game logic updates."""
        pass
