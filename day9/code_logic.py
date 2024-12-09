from collections import deque
from functools import reduce
from itertools import chain
import math
import os.path
import re
from typing import List, Tuple
import dotenv

from utils.utils import get_input_if_not_exists, read_input_lines

dotenv.load_dotenv()


def get_first_dot_index(space_list: List[str]) -> int:
    for idx, char in enumerate(space_list):
        if char == ".":
            return idx
    raise ValueError("No dot found in list")


def get_last_digit_index(space_list: List[str]) -> int:
    for idx, char in enumerate(reversed(space_list)):
        if char.isdigit():
            return len(space_list) - idx - 1
    raise ValueError("No digits found in list")


def split_string(string: str) -> List[str]:
    return [char for char in string]


## Implementation of PART 1


def solve_level1(filename: str):
    lines = read_input_lines(filename)[0]
    chained_items = chain.from_iterable(
        zip(
            [
                str(idx) * int(char) if char != "0" else []
                for idx, char in enumerate(lines[::2])
            ],
            ["." * int(char) if char != "0" else [] for char in lines[1::2]] + ["."],
        )
    )

    space_str = "".join([string for string in chained_items if len(string) > 0])

    while not re.match(r"^\d+(\.+)$", space_str):

        first_dot_idx = get_first_dot_index(space_str)
        last_digit_index = get_last_digit_index(space_str)
        space_list = split_string(space_str)
        space_list[first_dot_idx] = space_list[last_digit_index]
        space_list[last_digit_index] = "."
        space_str = "".join(space_list)

    return sum([int(char) * idx for idx, char in enumerate(space_str) if char != "."])


## Implementation of PART 2


def solve_level2(filename: str):
    lines = read_input_lines(filename)
    result = 2
    return result


if __name__ == "__main__":

    current_directory = os.path.dirname(__file__)

    sample_file = f"{current_directory}/sample1.txt"
    filename1 = f"{current_directory}/input1.txt"
    filename2 = f"{current_directory}/input2.txt"

    # get_input_if_not_exists(2024, current_directory, 1)
    print(solve_level1(filename1))
    # get_input_if_not_exists(2024, current_directory, 2)
    # print(solve_level2(filename2))
