"""
This file defines the necessary functions and definitions that students must
import in order to be able to write a new Karel program. Any new Karel file
must include the following line:

from stanfordkarel import *

Original Author: Nicholas Bowman
Credits: Kylie Jue, Tyler Yep
License: MIT
Version: 1.0.0
Email: nbowman@stanford.edu
Date of Creation: 10/1/2019
"""

from collections.abc import Callable

from .karel_image_renderer import KarelImageRenderer
from .karel_program import KarelProgram
from .student_code import StudentCode

# The following function definitions are defined as stubs so that IDEs can recognize
# the function definitions in student code. These names are re-bound upon program
# execution to associate their behavior to the one particular Karel object located
# in a given world.


def move() -> None:
    raise NotImplementedError


def turn_left() -> None:
    raise NotImplementedError


def put_beeper() -> None:
    raise NotImplementedError


def pick_beeper() -> None:
    raise NotImplementedError


def front_is_clear() -> bool:
    raise NotImplementedError


def front_is_blocked() -> bool:
    raise NotImplementedError


def left_is_clear() -> bool:
    raise NotImplementedError


def left_is_blocked() -> bool:
    raise NotImplementedError


def right_is_clear() -> bool:
    raise NotImplementedError


def right_is_blocked() -> bool:
    raise NotImplementedError


def beepers_present() -> bool:
    raise NotImplementedError


def no_beepers_present() -> bool:
    raise NotImplementedError


def beepers_in_bag() -> bool:
    raise NotImplementedError


def no_beepers_in_bag() -> bool:
    raise NotImplementedError


def facing_north() -> bool:
    raise NotImplementedError


def not_facing_north() -> bool:
    raise NotImplementedError


def facing_east() -> bool:
    raise NotImplementedError


def not_facing_east() -> bool:
    raise NotImplementedError


def facing_west() -> bool:
    raise NotImplementedError


def not_facing_west() -> bool:
    raise NotImplementedError


def facing_south() -> bool:
    raise NotImplementedError


def not_facing_south() -> bool:
    raise NotImplementedError


def paint_corner(color: str) -> None:
    del color


def corner_color_is(color: str) -> bool:
    del color
    return True


# Defined constants for ease of use by students when coloring corners
RED = "Red"
BLACK = "Black"
CYAN = "Cyan"
DARK_GRAY = "Dark Gray"
GRAY = "Gray"
GREEN = "Green"
LIGHT_GRAY = "Light Gray"
MAGENTA = "Magenta"
ORANGE = "Orange"
PINK = "Pink"
WHITE = "White"
BLUE = "Blue"
YELLOW = "Yellow"
BLANK = ""


def run_karel_program(
    world_url: str | None = None,
    main_func: Callable[[], None] | None = None,
    world_text: str = "",
    cell_size: int = 50,
    speed: int | None = None,
) -> None:
    if main_func is None:
        raise ValueError(
            "main_func= is required.\n"
            "Example: run_karel_program(world_text='...', main_func=main)"
        )

    if speed is not None and not 0 <= speed <= 100:
        raise ValueError(f"speed must be between 0 and 100, got {speed}.")

    karel = KarelProgram(world_url=world_url, world_text=world_text)
    if speed is not None:
        karel.world.init_speed = speed

    renderer = KarelImageRenderer(karel.world, karel, cell_size=cell_size)
    student_code = StudentCode(main_func=main_func)
    renderer.run_and_render_to_ipython(student_code)
