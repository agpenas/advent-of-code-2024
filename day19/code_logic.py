import os.path
import re
from collections import defaultdict
from itertools import chain
from typing import Dict, List, Tuple

import dotenv
from tqdm import tqdm
from utils.utils import get_input_if_not_exists, read_input_lines

dotenv.load_dotenv()


## Implementation of PART 1


class TowelPattern:
    def __init__(
        self,
        pattern: str,
        available_subpatterns: List[str],
        cache: Dict[str, int] = None,
    ):
        self.initial_pattern = pattern
        self.available_subpatterns = available_subpatterns
        self.unavailable_subpatters = set()
        self.cache = cache if cache is not None else defaultdict(lambda: 0)

    def remove_subpatterns_iteratively(self, pattern: str = None):
        pattern = self.initial_pattern if pattern is None else pattern

        if pattern in self.cache:
            return self.cache[pattern]

        if pattern == "":
            return 1

        remaining_subpatterns = [
            pattern.removeprefix(subpattern)
            for subpattern in self.available_subpatterns
            if pattern.startswith(subpattern)
        ]

        if not remaining_subpatterns:
            self.unavailable_subpatters.add(pattern)
            return 0

        nb_combos = sum(
            [
                self.remove_subpatterns_iteratively(subpattern)
                for subpattern in remaining_subpatterns
            ]
        )
        self.cache[pattern] = nb_combos
        return nb_combos


def split_input_lines(lines: List[str]) -> Tuple[List[str], List[str]]:
    split_idx = [idx for idx, line in enumerate(lines) if line == ""][0]
    return lines[:split_idx], lines[split_idx + 1 :]


def solve_level1(filename: str):
    lines = read_input_lines(filename)
    subpatterns, patterns = split_input_lines(lines)
    subpatterns = list(
        map(
            str.strip,
            chain.from_iterable([subpattern.split(",") for subpattern in subpatterns]),
        )
    )
    feasible_patterns = list()
    for iter_nb, pattern in tqdm(enumerate(patterns)):
        cache = None if iter_nb == 0 else towel_pattern.cache
        towel_pattern = TowelPattern(pattern, subpatterns, cache)
        nb_possible_patterns = towel_pattern.remove_subpatterns_iteratively()
        feasible_patterns.append(nb_possible_patterns > 0)
    return sum(feasible_patterns)


## Implementation of PART 2


def solve_level2(filename: str):
    lines = read_input_lines(filename)
    subpatterns, patterns = split_input_lines(lines)
    subpatterns = list(
        map(
            str.strip,
            chain.from_iterable([subpattern.split(",") for subpattern in subpatterns]),
        )
    )
    feasible_patterns = list()
    for iter_nb, pattern in tqdm(enumerate(patterns)):
        cache = None if iter_nb == 0 else towel_pattern.cache
        towel_pattern = TowelPattern(pattern, subpatterns, cache)
        nb_possible_patterns = towel_pattern.remove_subpatterns_iteratively()
        feasible_patterns.append(nb_possible_patterns)

    return sum(feasible_patterns)


if __name__ == "__main__":

    current_directory = os.path.dirname(__file__)

    sample_file = f"{current_directory}/sample1.txt"
    filename1 = f"{current_directory}/input1.txt"
    filename2 = f"{current_directory}/input2.txt"

    # get_input_if_not_exists(2024, current_directory, 1)
    print(solve_level1(filename1))
    # get_input_if_not_exists(2024, current_directory, 2)
    print(solve_level2(filename1))
