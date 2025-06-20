from dataclasses import dataclass

@dataclass
class LevelResult:
    """
    Result of a level. Contains whether the player won and the time the level finished. Used by
    LevelScene to display the mission result. After a certain amount of time (defined as constant
    in LevelScene), the level scene will switch back to the menu scene.
    """
    player_won: bool
    finish_time: float