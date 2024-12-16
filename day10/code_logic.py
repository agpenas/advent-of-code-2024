import os.path
from typing import List, Tuple
import dotenv

from utils.utils import get_input_if_not_exists, read_input_lines

dotenv.load_dotenv()


## Implementation of PART 1


def get_initial_positions(array: List[List[str]]):
    initial_positions = list()
    for j, row in enumerate(array):
        for i, char in enumerate(row):
            if char != 0:
                continue
            initial_positions.append((i, j))
    return initial_positions


def recursive_climbing(position, array, valid_summits=list()):
    current_value = array[position[1]][position[0]]
    if current_value == 9:
        valid_summits.append(position)
        return valid_summits
    next_steps = list()
    for off_x, off_y in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        new_x, new_y = [position[0] + off_x, position[1] + off_y]
        if any([new_x < 0, new_y < 0, new_x >= len(array[0]), new_y >= len(array)]):
            continue
        if array[new_y][new_x] == current_value + 1:
            next_steps.append((new_x, new_y))
    if not next_steps:
        return valid_summits
    for new_x, new_y in next_steps:
        recursive_climbing(
            (new_x, new_y),
            array,
            valid_summits,
        )

    return valid_summits


def solve_level1(filename: str):
    lines = read_input_lines(filename)
    array = [[int(char) for char in line] for line in lines]
    initial_pos_list = get_initial_positions(array)
    result = 0
    for initial_pos in initial_pos_list:

        result += len(set(recursive_climbing(initial_pos, array, [])))

    return result


## Implementation of PART 2


def solve_level2(filename: str):
    lines = read_input_lines(filename)
    array = [[int(char) for char in line] for line in lines]
    initial_pos_list = get_initial_positions(array)
    result = 0
    for initial_pos in initial_pos_list:

        result += len(recursive_climbing(initial_pos, array, []))

    return result


if __name__ == "__main__":

    current_directory = os.path.dirname(__file__)

    sample_file = f"{current_directory}/sample1.txt"
    filename1 = f"{current_directory}/input1.txt"
    filename2 = f"{current_directory}/input2.txt"

    # get_input_if_not_exists(2024, current_directory, 1)
    # print(solve_level1(filename1))
    get_input_if_not_exists(2024, current_directory, 2)
    print(solve_level2(sample_file))
