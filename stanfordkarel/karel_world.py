"""
This file defines the class definition of a Karel world.

The sub header comment defines important notes about the Karel
world file format.

General Notes About World Construction
- Streets run EAST-WEST (rows)
- Avenues run NORTH-SOUTH (columns)

World File Constraints:
- World file should specify one component per line in the format
  KEYWORD: PARAMETERS
- Any lines with no colon delimiter will be ignored
- The accepted KEYWORD, PARAMETER combinations are as follows:
    - Dimension: (num_avenues, num_streets)
    - Wall: (avenue, street); direction
    - Beeper: (avenue, street) count
    - Karel: (avenue, street); direction
    - Color: (avenue, street); color
    - Speed: delay
    - BeeperBag: num_beepers
- Multiple parameter values for the same keyword should be separated by a semicolon
- All numerical values (except delay) must be expressed as ints. The exception
  to this is that the number of beepers can also be INFINITY
- Any specified color values must be valid TKinter color strings, and are limited
  to the set of colors
- Direction is case-insensitive and can be one of the following values:
    - East
    - West
    - North
    - South

Original Author: Nicholas Bowman
Credits: Kylie Jue, Tyler Yep
License: MIT
Version: 1.0.0
Email: nbowman@stanford.edu
Date of Creation: 10/1/2019
"""

from __future__ import annotations

import copy
import re
import urllib.request
from enum import Enum, unique
from typing import TYPE_CHECKING, Any, NamedTuple

if TYPE_CHECKING:
    from pathlib import Path

INFINITY = -1
COLOR_MAP = {
    "Red": "red",
    "Black": "black",
    "Cyan": "cyan",
    "Dark Gray": "gray30",
    "Gray": "gray55",
    "Green": "green",
    "Light Gray": "gray80",
    "Magenta": "magenta3",
    "Orange": "orange",
    "Pink": "pink",
    "White": "snow",
    "Blue": "blue",
    "Yellow": "yellow",
}
INIT_SPEED = 50
VALID_WORLD_KEYWORDS = [
    "dimension",
    "wall",
    "beeper",
    "karel",
    "speed",
    "beeperbag",
    "color",
]
KEYWORD_DELIM = ":"
PARAM_DELIM = ";"


class KarelWorld:
    def __init__(
        self,
        world_url: str | None = None,
        world_text: str = "",
    ) -> None:
        """
        Karel World constructor
        Parameters:
            world_url: URL to fetch the world definition from
            world_text: world definition as a string (alternative to world_url)
        """
        # Map of beeper locations to the count of beepers at that location
        self.beepers: dict[tuple[int, int], int] = {}

        # Map of corner colors, defaults to ""
        self.corner_colors: dict[tuple[int, int], str] = {}

        # Set of Wall objects placed in the world
        self.walls: set[Wall] = set()

        # Dimensions of the world
        self.num_streets = 1
        self.num_avenues = 1

        # Initial Karel state saved to enable world reset
        self.karel_start_location = (1, 1)
        self.karel_start_direction = Direction.EAST
        self.karel_start_beeper_count = 0

        # Initial speed slider setting
        self.init_speed = INIT_SPEED

        # Load world from inline text or URL
        if world_text:
            self.load_from_text(world_text)
        elif world_url is not None:
            self.load_from_url(world_url)
        else:
            raise ValueError(
                "Either world_url or world_text must be provided.\n"
                "Example: run_karel_program("
                "world_text='Dimension: (5, 5)\\nKarel: (1, 1); east', main_func=main)"
            )

        # Save initial beeper state to enable world reset
        self.init_beepers = copy.deepcopy(self.beepers)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, KarelWorld):
            return (
                self.num_streets == other.num_streets
                and self.num_avenues == other.num_avenues
                and self.walls == other.walls
                and self.beepers == other.beepers
                and self.corner_colors == other.corner_colors
            )
        return NotImplemented

    def __hash__(self) -> int:
        return 0

    @staticmethod
    def get_alt_wall(wall: Wall) -> Wall:
        if wall.direction == Direction.NORTH:
            return Wall(wall.avenue, wall.street + 1, Direction.SOUTH)
        if wall.direction == Direction.SOUTH:
            return Wall(wall.avenue, wall.street - 1, Direction.NORTH)
        if wall.direction == Direction.EAST:
            return Wall(wall.avenue + 1, wall.street, Direction.WEST)
        if wall.direction == Direction.WEST:
            return Wall(wall.avenue - 1, wall.street, Direction.EAST)
        raise ValueError

    @staticmethod
    def parse_parameters(keyword: str, param_str: str) -> dict[str, Any]:
        params: dict[str, Any] = {}
        for param_with_spaces in param_str.split(PARAM_DELIM):
            param = param_with_spaces.strip()

            # check to see if parameter encodes a location
            coordinate = re.match(r"\((\d+),\s*(\d+)\)", param)
            if coordinate:
                # avenue, street
                params["location"] = int(coordinate.group(1)), int(coordinate.group(2))
                continue

            # check to see if the parameter is a direction value
            if param in (d.value for d in Direction):
                params["direction"] = Direction(param)

            # check to see if parameter encodes a numerical value or color string
            elif keyword == "color":
                if param.title() not in COLOR_MAP:
                    raise ValueError(
                        f"Error: {param} is invalid parameter for {keyword}."
                    )
                params["color"] = param.title()

            # handle the edge case where Karel has infinite beepers
            elif param in ("infinity", "infinite") and keyword == "beeperbag":
                params["val"] = INFINITY

            # float values are only valid for the speed parameter.
            elif keyword == "speed":
                try:
                    params["val"] = int(100 * float(param))
                except ValueError as e:
                    raise ValueError(
                        f"Error: {param} is an invalid parameter for {keyword}."
                    ) from e

            # must be a digit then
            elif param.isdigit():
                params["val"] = int(param)

            else:
                raise ValueError(f"Error: {param} is invalid parameter for {keyword}.")
        return params

    def load_from_text(self, world_text: str) -> None:
        for i, line_with_spaces in enumerate(world_text.splitlines()):
            # Ignore blank lines and lines with no comma delineator
            line = line_with_spaces.strip()
            if not line:
                continue

            if KEYWORD_DELIM not in line:
                print(f"Incorrectly formatted - ignoring line {i} of file: {line}")
                continue

            keyword, param_str = line.lower().split(KEYWORD_DELIM)

            # only accept valid keywords as defined in world file spec
            params = self.parse_parameters(keyword, param_str)

            # handle all different possible keyword cases
            if keyword == "dimension":
                # set world dimensions based on location values
                self.num_avenues, self.num_streets = params["location"]

            elif keyword == "wall":
                # build a wall at the specified location
                (avenue, street), direction = (
                    params["location"],
                    params["direction"],
                )
                self.walls.add(Wall(avenue, street, direction))

            elif keyword == "beeper":
                # add the specified number of beepers to the world
                if params["location"] in self.beepers:
                    self.beepers[params["location"]] += params["val"]
                else:
                    self.beepers[params["location"]] = params["val"]

            elif keyword == "karel":
                # Give Karel initial state values
                self.karel_start_location = params["location"]
                self.karel_start_direction = params["direction"]

            elif keyword == "beeperbag":
                # Set Karel's initial beeper bag count
                self.karel_start_beeper_count = params["val"]

            elif keyword == "speed":
                # Set delay speed of program execution
                self.init_speed = params["val"]

            elif keyword == "color":
                # Set corner color to be specified color
                self.corner_colors[params["location"]] = params["color"]

            else:
                print(f"Invalid keyword - ignoring line {i} of world file: {line}")

    def load_from_url(self, world_url: str) -> None:
        with urllib.request.urlopen(str(world_url), timeout=30) as response:  # noqa: S310
            self.load_from_text(response.read().decode())

    def add_beeper(self, avenue: int, street: int) -> None:
        self.beepers[(avenue, street)] = self.beepers.get((avenue, street), 0) + 1

    def remove_beeper(self, avenue: int, street: int) -> None:
        if self.beepers.get((avenue, street), 0) > 0:
            self.beepers[(avenue, street)] -= 1
            if self.beepers[(avenue, street)] == 0:
                del self.beepers[(avenue, street)]

    def add_wall(self, wall: Wall) -> None:
        alt_wall = self.get_alt_wall(wall)
        if wall not in self.walls and alt_wall not in self.walls:
            self.walls.add(wall)

    def remove_wall(self, wall: Wall) -> None:
        alt_wall = self.get_alt_wall(wall)
        self.walls.discard(wall)
        self.walls.discard(alt_wall)

    def paint_corner(self, avenue: int, street: int, color: str) -> None:
        self.corner_colors[(avenue, street)] = color

    def corner_color(self, avenue: int, street: int) -> str:
        if (avenue, street) in self.corner_colors:
            return self.corner_colors[(avenue, street)]
        return ""

    def reset_corner(self, avenue: int, street: int) -> None:
        self.beepers.pop((avenue, street), None)
        self.corner_colors.pop((avenue, street), None)

    def wall_exists(self, avenue: int, street: int, direction: Direction) -> bool:
        wall = Wall(avenue, street, direction)
        return wall in self.walls

    def in_bounds(self, avenue: int, street: int) -> bool:
        return 0 < avenue <= self.num_avenues and 0 < street <= self.num_streets

    def reset_world(self) -> None:
        """Reset initial state of beepers in the world"""
        self.beepers = copy.deepcopy(self.init_beepers)
        self.corner_colors = {}

    def save_to_file(self, filepath: Path) -> None:
        # First, output dimensions of world
        output = f"Dimension: ({self.num_avenues}, {self.num_streets})\n"

        # Next, output all walls
        for wall in sorted(self.walls):
            output += f"Wall: ({wall.avenue}, {wall.street}); {wall.direction.value}\n"

        # Next, output all beepers
        for (x, y), count in sorted(self.beepers.items()):
            output += f"Beeper: ({x}, {y}); {count}\n"

        # Next, output all color information
        for (x, y), color in sorted(self.corner_colors.items()):
            if color:
                output += f"Color: ({x}, {y}); {color}\n"

        # Next, output Karel information
        output += (
            f"Karel: {self.karel_start_location}; {self.karel_start_direction.value}\n"
        )

        # Finally, output beeperbag info
        beeper_output = (
            self.karel_start_beeper_count
            if self.karel_start_beeper_count >= 0
            else "INFINITY"
        )
        output += f"BeeperBag: {beeper_output}\n"

        with filepath.open("w", encoding="utf-8") as f:
            f.write(output)


@unique
class Direction(Enum):
    EAST = "east"
    SOUTH = "south"
    WEST = "west"
    NORTH = "north"

    def __lt__(self, other: object) -> bool:
        """Required to sort Directions."""
        if isinstance(other, Direction):
            return self.value < other.value
        return NotImplemented

    def __repr__(self) -> str:
        return str(self.value)


class Wall(NamedTuple):
    """Walls are stored using west or south directions only (every wall can be expressed this way)."""  # noqa: E501

    avenue: int
    street: int
    direction: Direction
