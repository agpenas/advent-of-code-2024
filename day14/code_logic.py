from collections import Counter
from dataclasses import dataclass
from math import prod
import os.path
import re
from typing import List, Tuple
import dotenv
from tqdm import tqdm

from utils.utils import get_input_if_not_exists, read_input_lines

dotenv.load_dotenv()


## Implementation of PART 1
@dataclass
class Grid:
    max_x: int
    max_y: int

    def _verify_max_dim_are_odd(self):
        if self.max_x % 2 == 0 or self.max_y % 2 == 0:
            raise ValueError("Max dimensions should be odd numbers")

    def __post_init__(self):
        self._verify_max_dim_are_odd()
        self.mid_x = self.max_x // 2
        self.mid_y = self.max_y // 2

    def assign_quadrant(self, x, y):
        if x == self.mid_x or y == self.mid_y:
            return None
        return int(x > self.mid_x) + 2 * int(y > self.mid_y)


@dataclass
class Robot:
    x: int
    y: int
    dx: int
    dy: int
    grid: Grid

    def _move_one_step(self):
        self.x += self.dx
        self.y += self.dy

    def _teleport_if_out_of_grid(self):
        if self.x < 0:
            self.x += self.grid.max_x

        if self.y < 0:
            self.y += self.grid.max_y

        if self.x >= self.grid.max_x:
            self.x %= self.grid.max_x

        if self.y >= self.grid.max_y:
            self.y %= self.grid.max_y

    def move_n_steps(self, n):
        for _ in range(n):
            self._move_one_step()
            self._teleport_if_out_of_grid()

    def _get_quadrant(self):
        return self.grid.assign_quadrant(self.x, self.y)


def parse_line(string: str):
    integers = list(map(int, re.findall(r"-?\d+", string)))
    return integers


def solve_level1(filename: str, grid_max_x, grid_max_y):
    parsed_lines = [parse_line(line) for line in read_input_lines(filename)]
    grid = Grid(grid_max_x, grid_max_y)
    robots_list = [Robot(*integers, grid) for integers in parsed_lines]
    for robot in robots_list:
        robot.move_n_steps(100)

    quadrants = [robot._get_quadrant() for robot in robots_list]
    quadrants_counter = Counter([quad for quad in quadrants if isinstance(quad, int)])
    safety_factor = prod(quadrants_counter.values())
    return safety_factor


## Implementation of PART 2


def print_grid(robots_list: List[Robot], grid: Grid):
    grid_matrix = [["." for _ in range(grid.max_x)] for _ in range(grid.max_y)]
    for robot in robots_list:
        grid_matrix[robot.y][robot.x] = "X"

    for row in grid_matrix:
        print("".join(row))


def is_potential_tree_trunk(robots_list: List[Robot], min_detected_lines: int):
    # Check for vertical lines !
    detected_lines = 0
    robot_positions_set = {(robot.x, robot.y) for robot in robots_list}
    for idx, robot in enumerate(robots_list):
        for vertical_offset in range(1, 6, 1):
            if not (robot.x, robot.y + vertical_offset) in robot_positions_set:
                break
            if vertical_offset == 5:
                detected_lines += 1
                print(idx, robot)
        if detected_lines >= min_detected_lines:
            return True
    return False


def solve_level2(filename: str, grid_max_x, grid_max_y):
    parsed_lines = [parse_line(line) for line in read_input_lines(filename)]
    grid = Grid(grid_max_x, grid_max_y)
    robots_list = [Robot(*integers, grid) for integers in parsed_lines]
    for step in tqdm(range(10_000)):
        for robot in robots_list:
            robot.move_n_steps(1)
        if is_potential_tree_trunk(robots_list, 2):
            print(step, "\n")
            print_grid(robots_list, grid)
            print("\n")
            # Found after 6242 steps !!

    quadrants = [robot._get_quadrant() for robot in robots_list]
    quadrants_counter = Counter([quad for quad in quadrants if isinstance(quad, int)])
    safety_factor = prod(quadrants_counter.values())
    return safety_factor


if __name__ == "__main__":

    current_directory = os.path.dirname(__file__)

    sample_file = f"{current_directory}/sample1.txt"
    filename1 = f"{current_directory}/input1.txt"
    filename2 = f"{current_directory}/input2.txt"

    get_input_if_not_exists(2024, current_directory, 1)
    # print(solve_level1(sample_file, 11, 7))
    # print(solve_level1(filename1, 101, 103))
    get_input_if_not_exists(2024, current_directory, 2)
    print(solve_level2(filename2, 101, 103))
