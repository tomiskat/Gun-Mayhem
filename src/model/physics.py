from dataclasses import dataclass
from functools import cached_property


@dataclass
class Physics:
    """
    Stores the physical properties of the game. Tuned for 2560x1600 resolution, with scaling
    applied for others. Each entity uses its own Physics instance, allowing easy future
    customization (e.g., higher jump, different speed).
    """
    BASE_WIDTH: int = 2560
    BASE_HEIGHT: int = 1600

    gravity: float = 1.0
    move_speed: float = 10.0
    jump_speed: float = -22.0
    bullet_speed: float = 15.0
    bullet_damage: float = 50.0

    animation_speed = 0.2
    knockback_decay = 0.9
    knockback_threshold = 0.1

    def apply_scaling(self, screen_width: int, screen_height: int):
        """
        Scales the physical properties according to the screen size.
        """
        scale_x = screen_width / self.BASE_WIDTH
        scale_y = screen_height / self.BASE_HEIGHT

        self.gravity *= scale_y
        self.move_speed *= scale_x
        self.jump_speed *= scale_y
        self.bullet_speed *= scale_x
        self.bullet_damage *= scale_x

    @cached_property
    def jump_height(self) -> float:
        """
        Computes the jump height in pixels. Beware, the result is negative, because the jump moves
        upward. Please note that the result is cached to avoid repeated computation.If you already
        accessed the property and then change physics attributes that affect jump height (such as
        `gravity` or `jump_speed`), you must manually clear the cache by calling:

            del <variable_name>.__dict__['jump_height']

        where `<variable_name>` is your instance of the Physics class. This ensures the value is
        recalculated the next time it is accessed.
        """
        jump_height = 0
        v = self.jump_speed
        while v < 0:
            jump_height += v
            v += self.gravity
        return jump_height



