import copy
import os
import pygame

from src.constants import colors
from src.constants.fonts import LARGE_FONT
from src.constants.paths import MAP_PATH
from src.entities.enemies.enemy_factory import EnemyFactory
from src.entities.player import Player
from src.managers.game_manager import GameScenes, GameManager
from src.managers.level_manager import LevelManager
from src.model.entity_config import EntityConfig
from src.model.level_result import LevelResult
from src.model.physics import Physics
from src.scenes.scene import Scene
from src.ui.entity_panel import EntityPanel
from src.utils.map_loader import MapLoader


class LevelScene(Scene):
    """
    Main game scene handling rendering and logic for a specific level.
    """
    SWITCH_TO_MENU_DELAY = 1000

    def __init__(self, surface: pygame.Surface, game_manager: GameManager, level_manager: LevelManager):
        super().__init__(surface, game_manager)
        self.level_manager = level_manager
        self._init_ui_layout()

    def _init_ui_layout(self):
        """
        Initialize sizes and spacing in panel that holds information about entities in the game.
        Each entity has its own panel.
        """
        self.panel_width = self.width // 10
        self.panel_height = self.height // 15
        self.spacing = self.panel_height // 8

    def initialize(self):
        """
        Initialize the level scene each time when the level is started from the menu.
        In case that level was paused, there is no need to reinitialize the level.
        """
        pygame.mouse.set_visible(False)
        if self.game_manager.previous_scene == GameScenes.PAUSE:
            return

        self._initialize()
        self._load_map()
        self._load_entities()
        self._create_ui_panels()

    def _initialize(self):
        """
        Initialize the level, level result, and bullet groups.
        """
        self.level = self.level_manager.current_level
        self.level_result = None
        self.player_bullets = pygame.sprite.Group()
        self.enemy_bullets = pygame.sprite.Group()

    def _load_map(self):
        map_path = os.path.join(MAP_PATH, self.level["map"])
        self.map_data = MapLoader.load_map(str(map_path), self.width, self.height)

    def _load_entities(self):
        """
        Load all entities in the level. Each entity will receive default physics which
        is scaled to the size of the map. The default physics was tuned for resolution
        2560x1600. See Physics class for more details.
        """
        physics = Physics()
        physics.apply_scaling(self.map_data.width, self.map_data.height)

        self._load_player(physics)
        self._load_enemies(physics)

    def _create_entity_config(self, physics, entity_data, bullet_adder):
        """
        Create a configuration object for an entity. Pass physics as copy to let each entity
        modify its physics (for example change move speed).
        """
        physics_copy = copy.copy(physics)
        return EntityConfig(self.map_data, entity_data, bullet_adder, physics_copy)

    def _load_player(self, physics):
        """
        Load player entity and place it into player group.
        """
        player_config = self._create_entity_config(physics, self.level["player"], self.player_bullets.add)
        self.player = Player(player_config)
        self.player_group = pygame.sprite.Group(self.player)

    def _load_enemies(self, physics):
        """
        Load all enemies in the level and place them into enemy group.
        """
        self.enemy_group = pygame.sprite.Group()
        for enemy_data in self.level["enemies"]:
            enemy_config = self._create_entity_config(physics, enemy_data, self.enemy_bullets.add)
            enemy = EnemyFactory.create_enemy(enemy_config)
            self.enemy_group.add(enemy)

    def update(self):
        """
        Update the level scene.
        """
        self.player_group.update()
        self.enemy_group.update(
            player_bullets=self.player_bullets,
            player_center=self.player.rect.centerx,
            player_platform=self.player.platform
        )
        self.player_bullets.update(self.map_data.width)
        self.enemy_bullets.update(self.map_data.width)
        self._check_bullet_collisions()
        self._check_level_end()

    def _check_bullet_collisions(self):
        self._handle_enemy_bullets()
        self._handle_friendly_bullets()

    def _handle_enemy_bullets(self):
        """
        If the player is hit by an enemy bullet, apply knockback.
        """
        hit_bullets = pygame.sprite.spritecollide(self.player, self.enemy_bullets, dokill=True)
        for bullet in hit_bullets:
            self.player.knockback_x += bullet.damage

    def _handle_friendly_bullets(self):
        """
        If enemy is hit by a player bullet, apply knockback.
        """
        hits = pygame.sprite.groupcollide(self.enemy_group, self.player_bullets, False, True)
        for enemy, bullets in hits.items():
            for bullet in bullets:
                enemy.knockback_x += bullet.damage

    def _check_level_end(self):
        """
        Check if the level is finished. In case that it is, check if it is time to switch
        to the menu. The level finishes when player or all enemies has no more lives.
        If entity is killed it is removed from the group.
        """
        if self.level_result:
            self._check_switch_to_menu()
            return

        if len(self.player_group) == 0:
            self.level_result = LevelResult(False, pygame.time.get_ticks())
        elif len(self.enemy_group) == 0:
            self.level_result = LevelResult(True, pygame.time.get_ticks())
            self.level_manager.unlock_next_level()

    def _check_switch_to_menu(self):
        """
        The level scene is switched to the menu scene after certain amount of time since level
        finishing has passed. (SWITCH_TO_MENU_DELAY = 1000 ms)
        """
        if pygame.time.get_ticks() - self.level_result.finish_time > self.SWITCH_TO_MENU_DELAY:
            self.game_manager.set_scene(GameScenes.MENU)

    def _create_ui_panels(self):
        """
        Create UI panels for all entities in the level. The UI panel holds information about
        entity (name, image and lives - this value is updated dynamically).
        """
        all_entities = [*self.player_group, *self.enemy_group]
        total_width = (self.panel_width + self.spacing) * len(all_entities) - self.spacing
        start_x = (self.width - total_width) // 2
        panel_size = (self.panel_width, self.panel_height)
        self.entity_panels = []

        for index, entity in enumerate(all_entities):
            x = start_x + index * (self.panel_width + self.spacing)
            y = self.spacing
            position = (x, y)
            entity_data = (entity.name, entity.image)
            panel = EntityPanel(panel_size, position, self.spacing, *entity_data)
            self.entity_panels.append((panel, entity))

    def handle_event(self, event):
        """
        Pause scene if player presses escape.
        """
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.game_manager.set_scene(GameScenes.PAUSE)

    def draw(self):
        """
        Draw the level. Start with drawing the map, then draw UI panels, then draw entities and finally
        draw bullets. If the level is finished, draw the mission result at the top of the surface.
        """
        self._draw_map()
        self._draw_ui()
        self._draw_entities()
        self._draw_bullets()

        if self.level_result:
            self._draw_mission_result()

    def _draw_map(self):
        self.surface.blit(self.map_data.surface, (0, 0))

    def _draw_ui(self):
        for panel, entity in self.entity_panels:
            panel.draw(self.surface, entity.lives)

    def _draw_entities(self):
        for entity in [*self.player_group, *self.enemy_group]:
            entity.draw(self.surface)

    def _draw_bullets(self):
        self.player_bullets.draw(self.surface)
        self.enemy_bullets.draw(self.surface)

    def _draw_mission_result(self):
        text, color = self._get_level_finish_text_and_color()
        mission_result = LARGE_FONT.render(text, True, color)
        rect = mission_result.get_rect(center=self.surface.get_rect().center)
        self.surface.blit(mission_result, rect)

    def _get_level_finish_text_and_color(self):
        if self.level_result.player_won:
            return "MISSION COMPLETED", colors.GREEN
        else:
            return "MISSION FAILED", colors.RED
