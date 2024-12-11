from collections import defaultdict
from dataclasses import dataclass
from itertools import chain
import os.path
from typing import List, Tuple
import dotenv
from tqdm import tqdm

from utils.utils import get_input_if_not_exists, read_input_lines

dotenv.load_dotenv()


## Implementation of PART 1
@dataclass
class MagicStone:
    number: int

    def _add_one(self):
        return self.number + 1

    def _mult_2024(self):
        return self.number * 2024

    def _split_number(self):
        str_number = str(self.number)
        half_nb_digits = len(str_number) // 2
        return list(
            map(int, [str_number[:half_nb_digits], str_number[half_nb_digits:]])
        )

    def blink(self):
        if self.number == 0:
            return [MagicStone(self._add_one())]
        elif len(str(self.number)) % 2 == 0:
            return [MagicStone(nb) for nb in self._split_number()]
        else:
            return [MagicStone(self._mult_2024())]


def solve_level1(filename: str):
    lines = read_input_lines(filename)[0]
    magic_stones_list = [MagicStone(int(str_nb)) for str_nb in lines.split()]
    for _ in range(25):
        blinked_stones = [stone.blink() for stone in magic_stones_list]
        magic_stones_list = list(chain.from_iterable(blinked_stones))

    return len(magic_stones_list)


## Implementation of PART 2


def recursive_stone_generator(magic_stone: MagicStone, nb_iter: int):
    if nb_iter == 1:
        yield magic_stone.blink()
    else:
        for stone in magic_stone.blink():
            yield from recursive_stone_generator(stone, nb_iter - 1)


def solve_level2(filename: str):
    lines = read_input_lines(filename)[0]
    nb_stones = 0
    magic_stones_list = [MagicStone(int(str_nb)) for str_nb in lines.split()]
    for initial_stone in magic_stones_list:
        print("Starting a new stone ! ")
        for final_stone_list in tqdm(recursive_stone_generator(initial_stone, 75)):
            nb_stones += len(final_stone_list)

    return nb_stones


if __name__ == "__main__":

    current_directory = os.path.dirname(__file__)

    sample_file = f"{current_directory}/sample1.txt"
    filename1 = f"{current_directory}/input1.txt"
    filename2 = f"{current_directory}/input2.txt"

    # get_input_if_not_exists(2024, current_directory, 1)
    # print(solve_level1(filename1))
    get_input_if_not_exists(2024, current_directory, 2)
    print(solve_level2(filename2))
