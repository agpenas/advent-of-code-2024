from collections import defaultdict
import math
import os.path
from typing import Dict, List, Set, Tuple
import dotenv

from utils.utils import get_input_if_not_exists, read_input_lines

dotenv.load_dotenv()


## Implementation of PART 1
def split_input(lines: List[str]) -> Tuple[List[str], List[str]]:
    split_idx = [idx for idx, line in enumerate(lines) if len(line) == 0]
    return lines[: split_idx[0]], lines[split_idx[0] + 1 :]


def create_rules_dict(rules: List[str]) -> Tuple[Dict[int, Set[int]]]:
    preceding_rules_dict = defaultdict(set)
    succeeding_rules_dict = defaultdict(set)
    for rule in rules:
        int1, int2 = map(int, rule.split("|"))
        succeeding_rules_dict[int1].add(int2)
        preceding_rules_dict[int2].add(int1)
    return succeeding_rules_dict, preceding_rules_dict


def validate_printing_order(
    prec_dict: Dict[int, Set[int]],
    succ_dict: Dict[int, Set[int]],
    printing_order: List[str],
) -> bool:
    for idx, item in enumerate(printing_order):
        if any([prec not in prec_dict[item] for prec in printing_order[:idx]]):
            return False
        if any([succ not in succ_dict[item] for succ in printing_order[idx + 1 :]]):
            return False
    return True


def solve_level1(filename: str):
    lines = read_input_lines(filename)
    rules, input = split_input(lines)
    input_formatted = [list(map(int, line.split(","))) for line in input]
    succ_dict, prec_dict = create_rules_dict(rules)
    valid_orders = [
        order
        for order in input_formatted
        if validate_printing_order(prec_dict, succ_dict, order)
    ]
    return sum([order[math.floor(len(order) / 2)] for order in valid_orders])


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
