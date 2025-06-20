import sys
import pygame
from src.constants.paths import MUSIC
from src.enums.game_scenes import GameScenes


class GameManager:
    """
    Manage game scenes, shared by all scenes. Used to handle scene changes and
    audio management.
    """

    def __init__(self) -> None:
        self._previous_scene = None
        self._current_scene = GameScenes.MENU
        self._audio_available = self.init_audio()

    @property
    def current_scene(self) -> GameScenes:
        return self._current_scene

    @property
    def previous_scene(self) -> GameScenes:
        return self._previous_scene

    def set_scene(self, game_scene: GameScenes) -> None:
        self._previous_scene = self.current_scene
        self._current_scene = game_scene

    @property
    def audio_available(self) -> bool:
        return self._audio_available

    def toggle_music(self):
        """
        Handle music change if audio is available.
        """
        if self._audio_available:
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.pause()
            else:
                pygame.mixer.music.unpause()

    @staticmethod
    def init_audio() -> bool:
        """
        Initialize pygame audio. If audio is not available, return False. (This happens
        when running code on wsl2.)
        """
        try:
            pygame.mixer.init()
            music_path = MUSIC
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.play(-1)
            return True

        except pygame.error as e:
            print(f"[Audio Error] Audio initialization failed: {e}", file=sys.stderr)
            return False
