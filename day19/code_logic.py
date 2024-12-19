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


class TowalPattern:
    def __init__(self, pattern: str, available_subpatterns: List[str], cache: Dict[str, int] = None):
        self.initial_pattern = pattern
        self.available_subpatterns = available_subpatterns
        self.unavailable_subpatters = set()
        self.cache = cache if cache is not None else defaultdict(lambda: 0)

    def remove_subpatterns_iteratively(self, pattern: str = None, previous_pattern: str = None):
        if pattern is None:
            pattern = self.initial_pattern
        if pattern not in self.unavailable_subpatters:
            if pattern == "":
                self.cache[previous_pattern] += 1
                print(previous_pattern)
                yield 1
            elif pattern in self.cache:
                print(previous_pattern)
                yield self.cache[pattern]
            else:
                valid_subpatterns = [
                    subpattern for subpattern in self.available_subpatterns if pattern.startswith(subpattern)
                ]
                if not valid_subpatterns:
                    self.unavailable_subpatters.add(pattern)
                else:
                    remaining_subpatterns = [pattern.removeprefix(subpattern) for subpattern in valid_subpatterns]
                    if all([subpattern in self.cache for subpattern in remaining_subpatterns]):
                        self.cache[pattern] = sum([self.cache[subpattern] for subpattern in remaining_subpatterns])
                    print(remaining_subpatterns)
                    for subpattern in remaining_subpatterns:
                        yield from self.remove_subpatterns_iteratively(
                            subpattern,
                            pattern,
                        )


def split_input_lines(lines: List[str]) -> Tuple[List[str], List[str]]:
    split_idx = [idx for idx, line in enumerate(lines) if line == ""][0]
    return lines[:split_idx], lines[split_idx + 1 :]


def solve_level1(filename: str):
    lines = read_input_lines(filename)
    subpatterns, patterns = split_input_lines(lines)
    subpatterns = list(map(str.strip, chain.from_iterable([subpattern.split(",") for subpattern in subpatterns])))
    feasible_patterns = list()
    for pattern in tqdm(patterns):
        towel_pattern = TowalPattern(pattern, subpatterns)
        nb_possible_patterns = list(towel_pattern.remove_subpatterns_iteratively())
        feasible_patterns.append(int(sum(nb_possible_patterns) > 0))
    return sum(feasible_patterns)


## Implementation of PART 2


def solve_level2(filename: str):
    lines = read_input_lines(filename)
    subpatterns, patterns = split_input_lines(lines)
    subpatterns = list(map(str.strip, chain.from_iterable([subpattern.split(",") for subpattern in subpatterns])))
    feasible_patterns = list()
    for pattern in tqdm(patterns):
        towel_pattern = TowalPattern(pattern, subpatterns)
        nb_possible_patterns = list(towel_pattern.remove_subpatterns_iteratively())
        feasible_patterns.append(sum(nb_possible_patterns))

    return sum(feasible_patterns)


if __name__ == "__main__":

    current_directory = os.path.dirname(__file__)

    sample_file = f"{current_directory}/sample1.txt"
    filename1 = f"{current_directory}/input1.txt"
    filename2 = f"{current_directory}/input2.txt"

    # get_input_if_not_exists(2024, current_directory, 1)
    # print(solve_level1(sample_file))
    # get_input_if_not_exists(2024, current_directory, 2)
    print(solve_level2(sample_file))
