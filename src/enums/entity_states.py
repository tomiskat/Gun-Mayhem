from enum import Enum, auto

class EntityState(Enum):
    """
    Images for individual entity states can be found in assets/images/entity/{player|enemy}
    """
    IDLE = auto()
    RUNNING = auto()
    JUMPING = auto()