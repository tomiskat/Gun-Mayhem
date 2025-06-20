import pygame

from src.managers.game_manager import GameManager, GameScenes
from src.managers.level_manager import LevelManager
from src.scenes.level_scene import LevelScene
from src.scenes.menu_scene import MenuScene
from src.scenes.pause_scene import PauseScene


class Game:
    """
    Main application class. Create scenes for individual game scenes and run the game loop.
    """
    def __init__(self):
        pygame.init()
        self.running = True
        self._init_display()
        self._load_scenes()
        self.scene = None

    def _init_display(self):
        """
        Set up the display to fullscreen mode and initialize the clock.
        """
        self.surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()

    def _load_scenes(self):
        """
        Load all scenes and initialize manager.
        """
        self.game_manager = GameManager()
        self.level_manager = LevelManager()
        self.scenes = {
            GameScenes.MENU: MenuScene(self.surface, self.game_manager, self.level_manager),
            GameScenes.LEVEL: LevelScene(self.surface, self.game_manager, self.level_manager),
            GameScenes.PAUSE: PauseScene(self.surface, self.game_manager),
        }

    def _check_scene_change(self):
        """
        Check if scene changed. If yes, initialize new scene and show it.
        """
        new_scene = self.scenes[self.game_manager.current_scene]
        if new_scene != self.scene:
            new_scene.initialize()
            self.scene = new_scene

    def _handle_events(self):
        """
        Handle all pygame events like keystrokes and mouse clicks.
        """
        for event in pygame.event.get():
            self.scene.handle_event(event)

    def _update(self):
        """
        Update scene (move entities, check collisions, etc.)
        """
        self.scene.update()

    def _draw(self):
        """
        Draw scene and show it (by flipping the surface)
        """
        self.scene.draw()
        pygame.display.flip()

    def run(self):
        """
        Main game loop.
        """
        while self.running:
            self._check_scene_change()
            self._handle_events()
            self._update()
            self._draw()
            self.clock.tick(60)


if __name__ == "__main__":
    app = Game()
    app.run()
