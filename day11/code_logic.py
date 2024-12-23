from collections import Counter, defaultdict
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


def recursive_stone_generator(magic_stone: MagicStone, nb_iter: int):
    if nb_iter == 1:
        yield magic_stone.blink()
    else:
        for stone in magic_stone.blink():
            yield from recursive_stone_generator(stone, nb_iter - 1)


def solve_level1(filename: str):
    lines = read_input_lines(filename)[0]
    nb_stones = 0
    numbers_counter = Counter([int(str_nb) for str_nb in lines.split()])
    for step in range(5):
        stone_counter = Counter()
        for iter_stone_nb, nb_stones in numbers_counter.items():
            iter_stone_counter = Counter(
                [
                    stone.number
                    for stone in chain.from_iterable(
                        recursive_stone_generator(MagicStone(iter_stone_nb), 5)
                    )
                ]
            )
            mult_counter = {k: v * nb_stones for k, v in iter_stone_counter.items()}
            stone_counter.update(mult_counter)
        numbers_counter = stone_counter

    return numbers_counter.total()


## Implementation of PART 2


def solve_level2(filename: str):
    lines = read_input_lines(filename)[0]
    nb_stones = 0
    numbers_counter = Counter([int(str_nb) for str_nb in lines.split()])
    for step in range(15):
        stone_counter = Counter()
        for iter_stone_nb, nb_stones in numbers_counter.items():
            iter_stone_counter = Counter(
                [
                    stone.number
                    for stone in chain.from_iterable(
                        recursive_stone_generator(MagicStone(iter_stone_nb), 5)
                    )
                ]
            )
            mult_counter = {k: v * nb_stones for k, v in iter_stone_counter.items()}
            stone_counter.update(mult_counter)
        numbers_counter = stone_counter

    return numbers_counter.total()


if __name__ == "__main__":

    current_directory = os.path.dirname(__file__)

    sample_file = f"{current_directory}/sample1.txt"
    filename1 = f"{current_directory}/input1.txt"
    filename2 = f"{current_directory}/input2.txt"

    # get_input_if_not_exists(2024, current_directory, 1)
    # print(solve_level1(filename1))
    get_input_if_not_exists(2024, current_directory, 2)
    print(solve_level2(sample_file))
