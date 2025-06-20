from src.weapons.triple_shotter import TripleShotter
from src.weapons.weapon import Weapon


class WeaponFactory:
    """
    Factory class for creating weapons based on the weapon name.
    """

    _weapon_classes = {
        "normal": Weapon,
        "triple": TripleShotter,
    }

    @staticmethod
    def get_weapon(weapon_name: str, on_bullet_created, bullet_images, bullet_speed, bullet_damage):
        weapon_class = WeaponFactory._weapon_classes.get(weapon_name.lower())
        return weapon_class(
            on_bullet_created=on_bullet_created,
            bullet_images=bullet_images,
            bullet_speed=bullet_speed,
            bullet_damage=bullet_damage
        )
