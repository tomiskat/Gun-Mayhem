import pygame

from typing import List
from src.constants import colors
from src.constants.fonts import LARGE_FONT
from src.managers.game_manager import GameManager, GameScenes
from src.managers.level_manager import LevelManager
from src.scenes.scene import Scene
from src.ui.button import Button


class MenuScene(Scene):
    """
    Game starting scene. It shows a title and buttons to start a level. Successfully finishing of
    the level will unlock next level.
    """

    def __init__(self, surface: pygame.Surface, game_manager: GameManager, level_manager: LevelManager):
        super().__init__(surface, game_manager)
        self.level_manager = level_manager
        self.buttons: List[Button] = []
        self._init_layout()

    def _init_layout(self):
        """
        Init components sizes and create them.
        """
        self.button_width = self.width // 3
        self.button_height = self.height // 15
        self.padding = self.button_height // 4
        self.title_height = LARGE_FONT.get_height()
        self.title_space = 3 * self.padding

        self._calculate_container_rect()
        self._set_title_position()
        self._create_level_buttons()

    def _calculate_container_rect(self):
        """
        Create and center the container that will hold game title and level buttons.
        """
        num_levels = len(self.level_manager.levels)
        total_button_height = num_levels * (self.button_height + self.padding) - self.padding
        container_height = self.title_height + self.title_space + total_button_height
        container_width = self.button_width

        x = (self.width - container_width) // 2
        y = (self.height - container_height) // 2
        self.container_rect = pygame.Rect(x, y, container_width, container_height)

    def _set_title_position(self):
        """
        Compute the position of the game title.
        """
        self.title_pos = (self.container_rect.centerx, self.container_rect.top + self.title_height // 2)

    def _create_level_buttons(self):
        """
        Create the level button rects.
        """
        x = self.container_rect.left
        y = self.container_rect.top + self.title_height + self.title_space
        button_dimensions = (self.button_width, self.button_height)

        for i, level in enumerate(self.level_manager.levels):
            button_rect = pygame.Rect(x, y + i * (self.button_height + self.padding), *button_dimensions)
            self.buttons.append(Button(button_rect, on_click=self._make_level_callback(level)))

    def _make_level_callback(self, level):
        """
        Handle level button click. If relevant level is unlocked, set it as the current level and
        switch to the level scene.
        """
        def callback():
            if level["unlocked"]:
                self.level_manager.current_level = level
                self.game_manager.set_scene(GameScenes.LEVEL)
        return callback

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.game_manager.set_scene(GameScenes.PAUSE)
            return

        for button in self.buttons:
            button.handle_event(event)

    def initialize(self):
        """
        Initialize the menu scene each time when game is switched to this scene.
        """
        super().initialize()
        self._render_title()
        self._render_level_buttons()

    def _render_title(self):
        title_text = LARGE_FONT.render("Gun Mayhem", True, colors.TITLE_COLOR)
        title_rect = title_text.get_rect(center=self.title_pos)
        self.surface.blit(title_text, title_rect)

    def _render_level_buttons(self):
        for i, button in enumerate(self.buttons):
            level = self.level_manager.levels[i]
            base_color, text_color = self._get_button_colors(level["unlocked"])
            button.draw(self.surface, level["name"], base_color, text_color)
            pygame.draw.rect(self.surface, (0, 0, 0), button.rect, 2, border_radius=10)

    @staticmethod
    def _get_button_colors(unlocked: bool):
        if unlocked:
            return colors.BUTTON_ENABLED, colors.WHITE
        return colors.BUTTON_DISABLED, colors.GRAY
