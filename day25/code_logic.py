from itertools import batched, product
import os.path
from typing import List, Tuple
import dotenv

from utils.utils import get_input_if_not_exists, read_input_lines

dotenv.load_dotenv()


## Implementation of PART 1


def split_input_lines(lines: List[str]) -> List[Tuple[str]]:
    lines += [""]
    return [block[:-1] for block in batched(lines, 8)]


def count_block_heights(block: List[str]) -> int:
    return [sum([line[idx] == "#" for line in block]) for idx in range(len(block[0]))]


def classify_blocks(blocks: List[str]) -> str:
    locks, keys = list(), list()
    for block in blocks:
        if "#" in block[0]:
            locks.append(count_block_heights(block))
            continue
        keys.append(count_block_heights(block))
    return locks, keys


def solve_level1(filename: str):
    lines = read_input_lines(filename)
    key_lock_blocks = split_input_lines(lines)
    locks, keys = classify_blocks(key_lock_blocks)
    max_height = len(key_lock_blocks[0])
    nb_valid_combinations = 0
    for lock, key in product(locks, keys):
        nb_valid_combinations += all(
            [lock[idx] + key[idx] <= max_height for idx in range(len(lock))]
        )

    return nb_valid_combinations


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

    get_input_if_not_exists(2024, current_directory, 1)
    print(solve_level1(filename1))
    # get_input_if_not_exists(2024, current_directory, 2)
    # print(solve_level2(filename2))
