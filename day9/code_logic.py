import math
import os.path
import re
from collections import deque
from functools import reduce
from itertools import chain, zip_longest
from typing import List, Tuple

import dotenv
from utils.utils import get_input_if_not_exists, read_input_lines

dotenv.load_dotenv()


## Implementation of PART 1


def solve_level1(filename: str):
    lines = read_input_lines(filename)[0]
    files_list, spaces_list = split_input_line(lines)
    moved_files = list()

    for spaces_idx in range(len(spaces_list)):

        relocated_files = list()

        while spaces_list[spaces_idx] > 0:

            relocated_files.append(files_list[-1].pop(-1))
            spaces_list[spaces_idx] -= 1

            if len(files_list[-1]) == 0:
                files_list.pop(-1)

        moved_files.append(relocated_files)

        if len(files_list) <= len(moved_files) + 1:
            break

    return calculate_checksum(files_list, moved_files)


def split_input_line(lines):
    files_list = [
        [idx] * int(char) if char != "0" else [] for idx, char in enumerate(lines[::2])
    ]
    spaces_list = [int(char) for char in lines[1::2]]
    return files_list, spaces_list


def calculate_checksum(
    files_list: List[List[int]], moved_files: List[List[int]]
) -> int:
    return sum(
        [
            int(char) * idx
            for idx, char in enumerate(
                chain.from_iterable(
                    chain.from_iterable(
                        zip_longest(files_list, moved_files, fillvalue=[])
                    )
                )
            )
        ]
    )


## Implementation of PART 2


def solve_level2(filename: str):

    lines = read_input_lines(filename)[0]

    files_list, spaces_list = split_input_line(lines)

    moved_files = [list() for _ in range(len(files_list))]

    for file_block_idx in range(len(files_list) - 1, 0, -1):

        file_block_length = len(files_list[file_block_idx])

        alloc_index = search_spaceful_slot_idx(
            spaces_list, file_block_length, file_block_idx
        )

        if alloc_index == -1:
            continue

        spaces_list[alloc_index] -= file_block_length
        moved_files[alloc_index].extend(files_list[file_block_idx])
        files_list[file_block_idx] = [0] * file_block_length

    moved_files_with_spaces = [
        files + [0] * nb_spaces if nb_spaces else files
        for files, nb_spaces in zip_longest(moved_files, spaces_list)
    ]
    return calculate_checksum(files_list, moved_files_with_spaces)


def search_spaceful_slot_idx(
    spaces_list: List[int], required_space: int, remaining_file_blocks: int
) -> int:
    for idx, space in enumerate(spaces_list):
        if space >= required_space and idx < remaining_file_blocks:
            return idx
    return -1


if __name__ == "__main__":

    current_directory = os.path.dirname(__file__)

    sample_file = f"{current_directory}/sample1.txt"
    filename1 = f"{current_directory}/input1.txt"
    filename2 = f"{current_directory}/input2.txt"

    get_input_if_not_exists(2024, current_directory, 1)
    print(solve_level1(filename1))
    get_input_if_not_exists(2024, current_directory, 2)
    print(solve_level2(filename2))
