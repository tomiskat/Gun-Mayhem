from typing import Type

from src.entities.enemies.enemy import Enemy
from src.entities.enemies.shrinker import Shrinker
from src.entities.enemies.invisible import Invisible
from src.model.entity_config import EntityConfig


class EnemyFactory:
    """
    Create an enemy instance based on the type specified in the config.
    """

    _enemy_classes: dict[str, Type[Enemy]] = {
        "default": Enemy,
        "shrinker": Shrinker,
        "invisible": Invisible,
    }

    @classmethod
    def create_enemy(cls, config: EntityConfig) -> Enemy:
        enemy_type = config.entity_data.get("type")
        enemy_class = cls._enemy_classes.get(enemy_type)
        return enemy_class(config)
