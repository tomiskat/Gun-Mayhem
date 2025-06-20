import pygame
from dataclasses import dataclass
from typing import Dict, List

@dataclass
class MapData:
    """
    Holds map data including dimensions, surface, and platform collision rects.
    Please beware that map dimensions are same as surface dimensions.
    """
    rows: int
    cols: int
    width: int
    height: int
    surface: pygame.Surface
    platforms: Dict[int, List[pygame.Rect]]