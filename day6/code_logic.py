import os.path
from typing import List, OrderedDict, Tuple
import dotenv

from utils.utils import get_input_if_not_exists, read_input_lines

dotenv.load_dotenv()


## Implementation of PART 1
class Directions:
    dir_dict = OrderedDict(
        [
            ("^", (0, -1)),
            (">", (1, 0)),
            ("v", (0, 1)),
            ("<", (-1, 0)),
        ]
    )
    dir_symbols_list = list(dir_dict.keys())

    def __init__(self, first_dir_symbol: str):
        self.current_dir_symbol = first_dir_symbol
        self.current_dir_tuple = self.dir_dict[first_dir_symbol]

    def turn_right(self):
        idx = self.dir_symbols_list.index(self.current_dir_symbol)
        self.current_dir_symbol = self.dir_symbols_list[
            (idx + 1) % len(self.dir_symbols_list)
        ]
        self.current_dir_tuple = self.dir_dict[self.current_dir_symbol]

    def forward_position(self, position_tuple: Tuple[int, int]) -> Tuple[int, int]:
        x, y = position_tuple
        dx, dy = self.current_dir_tuple
        return (x + dx, y + dy)

    def backward_position(self, position_tuple: Tuple[int, int]) -> Tuple[int, int]:
        x, y = position_tuple
        dx, dy = self.current_dir_tuple
        return (x - dx, y - dy)


def get_obstacles_coords(lines: List[str]) -> List[Tuple[int, int]]:
    obstacles = []
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char == "#":
                obstacles.append((x, y))
    return obstacles


def get_initial_coords_and_symbol(lines: List[str]) -> Tuple[Tuple[int, int], str]:
    field_symbolds = {".", "#"}
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char not in field_symbolds:
                return (x, y), char
    return None


def get_guard_path(
    guard_coords: Tuple[int, int],
    obstacle_coords: List[Tuple[int, int]],
    guard_symbol: str,
    grid_dimensions: Tuple[int, int],
) -> List[Tuple[int, int]]:
    obstacle_set = set(obstacle_coords)
    max_x, max_y = grid_dimensions
    guard_path = list()
    directions = Directions(guard_symbol)
    x, y = guard_coords
    while x < max_x and x >= 0 and y < max_y and y >= 0:
        x, y = directions.forward_position((x, y))
        if (x, y) in obstacle_set:
            x, y = directions.backward_position((x, y))
            directions.turn_right()
        else:
            guard_path.append((x, y))
    return set(guard_path[:-1])


def solve_level1(filename: str):
    lines = read_input_lines(filename)
    grid_dimensions = (len(lines[0]), len(lines))
    obstacle_coords = get_obstacles_coords(lines)
    guard_coords, guard_symbol = get_initial_coords_and_symbol(lines)
    guard_path_set = get_guard_path(
        guard_coords, obstacle_coords, guard_symbol, grid_dimensions
    )

    return len(guard_path_set)


## Implementation of PART 2


def get_walk_path_until_exit_or_loop(
    guard_coords: Tuple[int, int],
    obstacle_coords: List[Tuple[int, int]],
    guard_symbol: str,
    grid_dimensions: Tuple[int, int],
) -> List[Tuple[int, int]]:
    obstacle_set = set(obstacle_coords)
    max_x, max_y = grid_dimensions
    guard_path = list()
    directions = Directions(guard_symbol)
    x, y = guard_coords
    while x < max_x and x >= 0 and y < max_y and y >= 0:
        x, y = directions.forward_position((x, y))
        if (x, y) in obstacle_set:
            x, y = directions.backward_position((x, y))
            directions.turn_right()
        else:
            guard_path.append((x, y))
        if len(guard_path) > 10_000:
            return list()
    return guard_path


def solve_level2(filename: str):
    lines = read_input_lines(filename)
    grid_dimensions = (len(lines[0]), len(lines))
    obstacle_coords = get_obstacles_coords(lines)
    guard_coords, guard_symbol = get_initial_coords_and_symbol(lines)
    initial_guard_path = get_guard_path(
        guard_coords, obstacle_coords, guard_symbol, grid_dimensions
    )
    valid_obstacles = set()

    for new_obstacle_coords in initial_guard_path:
        guard_path_list = get_walk_path_until_exit_or_loop(
            guard_coords,
            obstacle_coords + [new_obstacle_coords],
            guard_symbol,
            grid_dimensions,
        )
        if not guard_path_list:
            valid_obstacles.add(new_obstacle_coords)

    return len(valid_obstacles.difference({guard_coords}))


if __name__ == "__main__":

    current_directory = os.path.dirname(__file__)

    sample_file = f"{current_directory}/sample1.txt"
    filename1 = f"{current_directory}/input1.txt"
    filename2 = f"{current_directory}/input2.txt"

    # get_input_if_not_exists(2024, current_directory, 1)
    # print(solve_level1(filename1))
    get_input_if_not_exists(2024, current_directory, 2)
    print(solve_level2(filename2))
