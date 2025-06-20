import pygame

from src.entities.enemies.enemy import Enemy
from src.model.entity_config import EntityConfig
class Invisible(Enemy):
    """
    Invisible enemy.

    This enemy remains invisible to the player except when shooting or being hit.
    Making it invisible even while shooting is possible, but keep in mind that the
    overridden draw method would need to manually advance the shooting animation's
    frame index. Otherwise, the entity would remain stuck in the 'shooting' state.
    This issue could also be addressed by changing the shooting logic (for example,
    by implementing a cooldown system for individual weapons).
    """
    def __init__(self, entity_config: EntityConfig):
        super().__init__(entity_config)

    def draw(self, surface: pygame.Surface):
        """
        Only draw the enemy when it's shooting or has been hit.
        """
        if self.knockback_x > 0 or self.shooting:
            super().draw(surface)

