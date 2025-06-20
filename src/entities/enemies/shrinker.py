from src.entities.enemies.enemy import Enemy
from src.model.entity_config import EntityConfig


class Shrinker(Enemy):
    """
    Shrinker enemy.

    This enemy is half the size of a normal enemy, making it harder to hit
    Its width and height are reduced after loading the base attributes.
    """
    def __init__(self, entity_config: EntityConfig):
        super().__init__(entity_config)

    def _load_entity_attributes(self):
        super()._load_entity_attributes()
        self.width //= 2
        self.height //= 2
