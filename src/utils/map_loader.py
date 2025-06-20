import pygame
import pytmx

from collections import defaultdict
from typing import Dict, List, Tuple
from pytmx.util_pygame import load_pygame
from src.constants.map_layers import PLATFORM_LAYER
from src.model.map_data import MapData
from src.utils.image_scaler import ImageScaler


class MapLoader:
    """
    Manages loading and caching of game maps.
    """
    _cache: Dict[Tuple[str, int, int], MapData] = {}

    @staticmethod
    def _get_scaled_rects(tmx: pytmx.TiledMap, scale: Tuple[float, float], layer_name: str) \
            -> Dict[int, List[pygame.Rect]]:
        """
        Extract and scale platform rectangles from TMX data. These platforms are then used
        for collision detection. For faster searching we use map to store platforms by
        a column index.
        """
        scale_x, scale_y = scale
        platforms = defaultdict(list)
        layer = tmx.get_layer_by_name(layer_name)

        if isinstance(layer, pytmx.TiledTileLayer):
            for x, y, gid in layer:
                if gid:
                    rect = pygame.Rect(
                        int(x * tmx.tilewidth * scale_x),
                        int(y * tmx.tileheight * scale_y),
                        int(tmx.tilewidth * scale_x),
                        int(tmx.tileheight * scale_y)
                    )
                    platforms[x].append(rect)

        return dict(platforms)

    @classmethod
    def _create_map(cls, surface: pygame.Surface, tmx: pytmx.TiledMap, width: int, height: int) -> MapData:
        """Create and return a MapData object from TMX data.

        Start by drawing all visible layers to a blank surface. Then scale the surface to given
        resolution, get platforms for collision detection and return the MapData object.
        """

        for layer in tmx.visible_layers:
            for x, y, gid in layer:
                if gid:
                    image = tmx.get_tile_image_by_gid(gid)
                    surface.blit(image, (x * tmx.tilewidth, y * tmx.tileheight))

        scale = (width / (tmx.width * tmx.tilewidth), height / (tmx.height * tmx.tileheight))
        surface = ImageScaler.scale_image(surface, width, height)
        platforms = cls._get_scaled_rects(tmx, scale, PLATFORM_LAYER)
        return MapData(tmx.height, tmx.width, *surface.get_size(), surface, platforms)

    @classmethod
    def load_map(cls, map_path: str, width: int, height: int) -> MapData:
        """
        Try to load a map from the cache. If not found, create a new MapData object and cache it.
        """
        key = (map_path, width, height)
        if key in cls._cache:
            return cls._cache[key]

        tmx = load_pygame(map_path)
        map_width = tmx.width * tmx.tilewidth
        map_height = tmx.height * tmx.tileheight
        surface = pygame.Surface((map_width, map_height))

        map_data = cls._create_map(surface, tmx, width, height)
        cls._cache[key] = map_data
        return map_data
