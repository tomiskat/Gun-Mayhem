import sys
import pygame

from src.constants import colors
from src.constants.paths import CONTROLS
from src.managers.game_manager import GameScenes, GameManager
from src.scenes.scene import Scene
from src.ui.button import Button
from src.utils.image_loader import ImageLoader
from src.utils.image_scaler import ImageScaler


class PauseScene(Scene):
    """
    A scene that is displayed when the game is paused by pressing the escape key. Its content
    is dynamically updated based on previous scene (when entered from a menu scene, the exit
    button will exit the whole game; when entered from a level scene, the exit button will
    return to the menu scene). This scene also contains a button to toggle the music.
    """

    def __init__(self, surface: pygame.Surface, game_manager: GameManager):
        super().__init__(surface, game_manager)
        self._load_controls_image()
        self._init_layout()

    def _load_controls_image(self):
        """
        Load image that tells the player how to play the game.
        """
        target_width = self.width // 3
        target_height = self.height // 2.5
        image = ImageLoader.load_image(CONTROLS)
        self.controls = ImageScaler.scale_image(image, target_width, target_height)

    def _init_layout(self):
        """
        Init pause scene components.
        """
        self.button_width = self.controls.get_width()
        self.button_height = self.height // 15
        self.button_spacing = self.button_height // 4
        self.component_spacing = 4 * self.button_spacing

        self._set_container_rect()
        self._set_image_rect()
        self._create_buttons()

    def _set_container_rect(self):
        """
        Create a container to hold the controls image, music toggle button, continue button
        and exit button.
        """
        spacing_height = 3 * self.component_spacing + 2 * self.button_spacing
        container_width = self.button_width + self.width // 20
        container_height = self.controls.get_height() + 3 * self.button_height + spacing_height
        self.container = pygame.Rect(0, 0, container_width, container_height)
        self.container.center = (self.width // 2, self.height // 2)

    def _set_image_rect(self):
        """
        Set the position of the controls image.
        """
        self.image_rect = self.controls.get_rect(
            centerx=self.width // 2,
            top=self.container.top + self.component_spacing
        )

    def _create_buttons(self):
        """
        Create toggle music, continue, and exit buttons.
        """
        x = (self.width - self.button_width) // 2
        y_start = self.image_rect.bottom + self.component_spacing
        vertical_spacing = self.button_height + self.button_spacing

        music_rect = pygame.Rect(x, y_start, self.button_width, self.button_height)
        continue_rect = pygame.Rect(x, y_start + 1 * vertical_spacing, self.button_width, self.button_height)
        exit_rect = pygame.Rect(x, y_start + 2 * vertical_spacing, self.button_width, self.button_height)

        self.music_button = Button(music_rect, on_click=self._handle_music_toggle)
        self.continue_button = Button(continue_rect, on_click=self._handle_continue)
        self.exit_button = Button(exit_rect, on_click=self._handle_exit)

    def _handle_music_toggle(self):
        """
        Redirect music toggling to the game manager. Also redraw content because the music
        button text might change.
        """
        self.game_manager.toggle_music()
        self._draw_content()

    def _handle_continue(self):
        """
        Change scene to previous scene. Used by continue button.
        """
        self.game_manager.set_scene(self.game_manager.previous_scene)

    def _handle_exit(self):
        """
        Handle exit button click. In case that previous scene is the level scene, return to
        menu scene. Otherwise, exit the game.
        """
        if self.game_manager.previous_scene == GameScenes.LEVEL:
            self.game_manager.set_scene(GameScenes.MENU)
        else:
            pygame.quit()
            sys.exit()

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self._handle_continue()
            return

        self.music_button.handle_event(event)
        self.continue_button.handle_event(event)
        self.exit_button.handle_event(event)

    def initialize(self):
        """
        In case that previous scene is the menu scene, draw the scene default background by using
        the parent draw() method. In case that level scene is paused, let level scene to be the
        background (Inspired by the original game.)
        """
        if self.game_manager.previous_scene == GameScenes.MENU:
            super().initialize()

        self._draw_overlay()
        self._draw_container()
        self._draw_content()

    def _draw_overlay(self):
        """
        Make background a little darker. (Used to make content in container better visible.)
        """
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill(colors.PAUSE_OVERLAY)
        self.surface.blit(overlay, (0, 0))

    def _draw_container(self):
        pygame.draw.rect(self.surface, colors.PAUSE_BG, self.container, border_radius=10)
        pygame.draw.rect(self.surface, colors.PAUSE_BORDER, self.container, 3, border_radius=10)

    def _draw_content(self):
        """
        Draw the scene content: the controls image, the music toggle button, the continue button
        and the exit button.
        """
        self.surface.blit(self.controls, self.image_rect)
        music_text, music_color = self._get_music_text_and_color()
        exit_text = "Quit game" if self.game_manager.previous_scene == GameScenes.MENU else "Return to menu"

        self.music_button.draw(self.surface, music_text, music_color)
        self.continue_button.draw(self.surface, "Continue", colors.BUTTON_CONTINUE)
        self.exit_button.draw(self.surface, exit_text, colors.BUTTON_EXIT)

    def _get_music_text_and_color(self):
        if not self.game_manager.audio_available:
            return "Audio unavailable", colors.BUTTON_DISABLED

        if pygame.mixer.music.get_busy():
            return "Music: On", colors.BUTTON_ENABLED
        else:
            return "Music: Off", colors.BUTTON_ENABLED
