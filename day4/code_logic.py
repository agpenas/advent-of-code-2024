from collections import Counter
from itertools import product
import os.path
from random import randint
from typing import List, Tuple
import dotenv

from utils.utils import get_input_if_not_exists, read_input_lines

dotenv.load_dotenv()


## Implementation of PART 1


def _verify_direction(list_of_coordinates: List[Tuple[int, ...]]):
    if len(list_of_coordinates) < 2:
        return True
    if len(set(x for x, _ in list_of_coordinates)) == 1:
        # All x are the same == horizontal direction
        return True
    if len(set(y for _, y in list_of_coordinates)) == 1:
        # All y are the same == vertical direction
        return True
    if len(set(x - y for x, y in list_of_coordinates)) == 1:
        # All x-y are the same == standard diagonal direction
        return True
    if len(set(x + y for x, y in list_of_coordinates)) == 1:
        # All x+y are the same == reverse diagonal direction
        return True
    return False


def recursive_expansive_search(
    grid: List[List[str]],
    x: int,
    y: int,
    letters_cumulated: str = "",
    coordinates_cumulated: List[Tuple[int]] = list(),
):
    if letters_cumulated not in "XMAS":
        return 0

    if letters_cumulated == "XMAS":
        return 1

    coordinates_to_inspect = [
        (new_x, new_y)
        for new_x, new_y in product(range(x - 1, x + 2), range(y - 1, y + 2))
        if all(
            [
                new_x >= 0 and new_y >= 0,
                (new_x, new_y) != (x, y),
                new_x < len(grid[0]) and new_y < len(grid),
                _verify_direction(coordinates_cumulated + [(new_x, new_y)]),
            ]
        )
    ]

    return sum(
        recursive_expansive_search(
            grid,
            new_x,
            new_y,
            letters_cumulated + grid[new_x][new_y],
            coordinates_cumulated + [(new_x, new_y)],
        )
        for new_x, new_y in coordinates_to_inspect
    )


def solve_level1(filename: str):
    lines = read_input_lines(filename)

    # Find all occurences of X
    initial_X_coords = [
        (row, col)
        for row, line in enumerate(lines)
        for col, char in enumerate(line)
        if char == "X"
    ]

    return sum(
        recursive_expansive_search(lines, x, y, "X", [(x, y)])
        for x, y in initial_X_coords
    )


## Implementation of PART 2


def verify_crossed_MAS(grid, x, y):
    coordinates_to_inspect = [
        (new_x, new_y)
        for new_x, new_y in product(range(x - 1, x + 2), range(y - 1, y + 2))
        if all(
            [
                new_x >= 0 and new_y >= 0,
                new_x != x,
                new_y != y,
                new_x < len(grid[0]) and new_y < len(grid),
            ]
        )
    ]
    if len(coordinates_to_inspect) < 4:
        return 0
    letters = [grid[new_x][new_y] for new_x, new_y in coordinates_to_inspect]

    if Counter(letters) != Counter("MMSS"):
        return 0
    if grid[x - 1][y - 1] == grid[x + 1][y + 1]:
        return 0
    return 1


def solve_level2(filename: str):
    lines = read_input_lines(filename)

    # Find all occurences of X
    initial_A_coords = [
        (row, col)
        for row, line in enumerate(lines)
        for col, char in enumerate(line)
        if char == "A"
    ]
    result = sum(verify_crossed_MAS(lines, x, y) for x, y in initial_A_coords)
    return result


if __name__ == "__main__":

    current_directory = os.path.dirname(__file__)

    sample_file = f"{current_directory}/sample1.txt"
    filename1 = f"{current_directory}/input1.txt"
    filename2 = f"{current_directory}/input2.txt"

    get_input_if_not_exists(2024, current_directory, 1)
    print(solve_level1(filename1))
    get_input_if_not_exists(2024, current_directory, 2)
    print(solve_level2(filename2))
