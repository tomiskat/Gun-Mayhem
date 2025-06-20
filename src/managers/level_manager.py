import glob
import os
from typing import Dict, List
from src.constants.paths import LEVEL_PATH
from src.utils.file_reader import FileReader
from src.utils.file_writer import FileWriter

class LevelManager:
    """
    Manage levels including loading, unlocking, and saving. Used by LevelScene
    and MenuScene (to set current level based on player click on level button).
    """

    def __init__(self):
        self._current_level = None
        self._levels: List[Dict] = []
        self._load_levels()

    @property
    def current_level(self) -> Dict:
        return self._current_level

    @current_level.setter
    def current_level(self, level: Dict) -> None:
        self._current_level = level

    @property
    def levels(self) -> List[Dict]:
        return self._levels

    def _load_levels(self) -> None:
        """
        Load levels from JSON files in levels directory.
        """
        pattern = os.path.join(LEVEL_PATH, '[0-9][0-9].json')
        level_files = sorted(glob.glob(pattern))
        self._levels = [FileReader.read_json(path) for path in level_files]

    def unlock_next_level(self) -> None:
        """
        Unlock the next level after the current one and save it.
        """
        current_id = self._current_level['id']
        next_id = current_id + 1

        if 0 < next_id < len(self._levels):
            next_level = self._levels[next_id]
            next_level['unlocked'] = True
            filename = f"{next_level['id'] + 1:02d}.json"
            path = os.path.join(LEVEL_PATH, filename)
            FileWriter.write_json(path, next_level)



