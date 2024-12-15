from dataclasses import dataclass
from itertools import chain
import os.path
import time
from typing import List, Tuple
import dotenv

from utils.utils import get_input_if_not_exists, read_input_lines

dotenv.load_dotenv()


## Implementation of PART 1


class Item:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y


class MovableItem(Item):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)

    def move(self, dx, dy):
        self.x += dx
        self.y += dy


class Box(MovableItem):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)

    def getGPS(self):
        return self.x + 100 * self.y

    def get_positions(self) -> List[Tuple[int, int]]:
        return [(self.x, self.y)]


class Grid:

    directions_mapping = {"v": (0, 1), "^": (0, -1), "<": (-1, 0), ">": (1, 0)}

    def __init__(
        self,
        box_coords: List[Tuple[int, int]],
        robot_coords: Tuple[int, int],
        obstacles: List[Tuple[int, int]],
    ):
        self.boxes = [Box(x, y) for x, y in box_coords]
        self.robot = MovableItem(*robot_coords)
        self.obstacles = [Item(x, y) for x, y in obstacles]
        self._update_positions_sets()
        self.max_x = max([x for x, _ in box_coords + [robot_coords] + obstacles])
        self.max_y = max([y for _, y in box_coords + [robot_coords] + obstacles])

    @classmethod
    def from_lines(cls, lines: List[str], box_char="O"):
        box_coords = []
        robot_coords = None
        obstacle_coords = []
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                if char == box_char:
                    box_coords.append((x, y))
                elif char == "@":
                    robot_coords = (x, y)
                elif char == "#":
                    obstacle_coords.append((x, y))
        return cls(box_coords, robot_coords, obstacle_coords)

    def _update_positions_sets(self):
        self.boxes_positions = set(
            chain.from_iterable(box.get_positions() for box in self.boxes)
        )
        self.obstacles_positions = {
            (obstacle.x, obstacle.y) for obstacle in self.obstacles
        }

    def attempt_robot_move(self, direction: str):
        dx, dy = self.directions_mapping[direction]
        boxes_in_path = set()
        for n_steps_ahead in range(1, self.max_y):

            next_position = (
                self.robot.x + n_steps_ahead * dx,
                self.robot.y + n_steps_ahead * dy,
            )

            if next_position in self.boxes_positions:
                boxes_in_path.add(next_position)
                continue
            if next_position in self.obstacles_positions:
                return
            break
        if boxes_in_path:
            for box in self.boxes:
                if (box.x, box.y) in boxes_in_path:
                    box.move(dx, dy)
            self._update_positions_sets()

        self.robot.move(dx, dy)

    def get_cumulative_gps(self):
        return sum([box.getGPS() for box in self.boxes])

    def print_grid(self):
        for y in range(self.max_y + 1):
            for x in range(self.max_x + 1):
                if (x, y) in self.boxes_positions:
                    print("O", end="")
                elif (x, y) in self.obstacles_positions:
                    print("#", end="")
                elif (x, y) == (self.robot.x, self.robot.y):
                    print("@", end="")
                else:
                    print(".", end="")
            print()


def solve_level1(filename: str):
    lines = read_input_lines(filename)
    splitting_line = lines.index("")
    grid = Grid.from_lines(lines[:splitting_line])
    movements = "".join(lines[splitting_line + 1 :])
    # grid.print_grid()
    for movement in movements:
        # print(movement)
        grid.attempt_robot_move(movement)
        # grid.print_grid()

    result = grid.get_cumulative_gps()

    return result


## Implementation of PART 2
class BigBox(Box):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.x2 = x + 1

    def getGPS(self):
        return self.x + 100 * self.y

    def move_large(self, dx, dy):
        self.move(dx, dy)
        self.x2 += dx

    def get_positions(self) -> List[Tuple[int, int]]:
        return [(self.x, self.y), (self.x2, self.y)]


class AugmentedGrid(Grid):
    augmentation_mapping = {
        "#": "##",
        "O": "[]",
        ".": "..",
        "@": "@.",
    }

    def __init__(
        self,
        box_coords: List[Tuple[int, int]],
        robot_coords: Tuple[int, int],
        obstacles: List[Tuple[int, int]],
    ):
        super().__init__(box_coords, robot_coords, obstacles)
        self.boxes = [BigBox(x, y) for x, y in box_coords]
        self._update_positions_sets()

    @classmethod
    def from_augmented_lines(cls, lines: List[str]):
        augmented_lines = [
            "".join([cls.augmentation_mapping[char] for char in line]) for line in lines
        ]
        return cls.from_lines(augmented_lines, box_char="[")

    def attempt_robot_move(self, direction: str):
        dx, dy = self.directions_mapping[direction]
        boxes_in_path = list()
        for n_steps_ahead in range(1, self.max_y):
            if not boxes_in_path:
                next_positions = {
                    (
                        self.robot.x + n_steps_ahead * dx,
                        self.robot.y + n_steps_ahead * dy,
                    )
                }
            else:
                last_boxes_positions = chain.from_iterable(
                    (box.get_positions() for box in next_step_boxes)
                )
                next_positions = {(x + dx, y + dy) for x, y in last_boxes_positions}
                next_step_boxes = list()

            if not next_positions.isdisjoint(self.obstacles_positions):
                return

            if not next_positions.isdisjoint(self.boxes_positions):
                next_step_boxes = [
                    box
                    for box in self.boxes
                    if (box.x, box.y) in next_positions
                    or (box.x2, box.y) in next_positions
                ]
                boxes_in_path.extend(next_step_boxes)
                continue

            break
        if boxes_in_path:
            for box in set(boxes_in_path):
                box.move_large(dx, dy)
            self._update_positions_sets()

        self.robot.move(dx, dy)

    def get_cumulative_gps(self):
        return sum([box.getGPS() for box in self.boxes])

    def print_augmented_grid(self):
        for y in range(self.max_y + 1):
            line = ""
            for x in range(self.max_x + 1):
                if (x, y) in self.boxes_positions:
                    if line[-1] == "[":
                        line += "]"
                    else:
                        line += "["
                elif (x, y) in self.obstacles_positions:
                    line += "#"
                elif (x, y) == (self.robot.x, self.robot.y):
                    line += "@"
                else:
                    line += "."
            print(line)


def solve_level2(filename: str):
    lines = read_input_lines(filename)
    splitting_line = lines.index("")
    grid = AugmentedGrid.from_augmented_lines(lines[:splitting_line])
    movements = "".join(lines[splitting_line + 1 :])
    # grid.print_augmented_grid()
    for movement in movements:
        # print(movement)
        grid.attempt_robot_move(movement)
        # grid.print_augmented_grid()

    result = grid.get_cumulative_gps()

    return result


if __name__ == "__main__":

    current_directory = os.path.dirname(__file__)

    sample_file = f"{current_directory}/sample1.txt"
    sample_file_2 = f"{current_directory}/sample2.txt"
    filename1 = f"{current_directory}/input1.txt"
    filename2 = f"{current_directory}/input2.txt"

    # get_input_if_not_exists(2024, current_directory, 1)
    # print(solve_level1(filename1))
    get_input_if_not_exists(2024, current_directory, 2)
    print(solve_level2(filename2))
