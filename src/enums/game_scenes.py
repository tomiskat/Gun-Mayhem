from enum import Enum, auto

class GameScenes(Enum):
    """
    Game scenes managed by the Game manager
    """
    MENU = auto()
    LEVEL = auto()
    PAUSE = auto()