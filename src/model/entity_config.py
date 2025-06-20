from dataclasses import dataclass
from typing import Callable
from src.model.map_data import MapData
from src.model.physics import Physics
from src.weapons.bullet import Bullet

@dataclass
class EntityConfig:
    """
    Configuration data for an entity (Enemy or Player).
    """
    map_data: MapData
    entity_data: dict
    on_bullet_created: Callable[[Bullet], None]
    physics: Physics