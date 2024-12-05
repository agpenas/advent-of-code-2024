from collections import defaultdict
from more_itertools import circular_shifts
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
) -> List[bool]:
    validity_list = list()
    for idx, item in enumerate(printing_order):
        if any([prec not in prec_dict[item] for prec in printing_order[:idx]]):
            validity_list.append(False)
            continue
        if any([succ not in succ_dict[item] for succ in printing_order[idx + 1 :]]):
            validity_list.append(False)
            continue
        validity_list.append(True)
    return validity_list


def solve_level1(filename: str):
    input_formatted, succ_dict, prec_dict = get_input_and_rules_dicts(filename)
    valid_orders = [
        order
        for order in input_formatted
        if all(validate_printing_order(prec_dict, succ_dict, order))
    ]
    return calculate_middle_item_sum(valid_orders)


def calculate_middle_item_sum(valid_orders):
    return sum([order[math.floor(len(order) / 2)] for order in valid_orders])


def get_input_and_rules_dicts(filename):
    lines = read_input_lines(filename)
    rules, input = split_input(lines)
    input_formatted = [list(map(int, line.split(","))) for line in input]
    succ_dict, prec_dict = create_rules_dict(rules)
    return input_formatted, succ_dict, prec_dict


## Implementation of PART 2


def fix_sequence(invalid_sequence: List[int], prec_dict, succ_dict):

    valid_list = list()
    # Rotate until the first element in the sublist is valid. We assume the set of rules is complete
    # and that there is only one valid shift even if we do not verify the already validated elements
    while len(invalid_sequence) > 0:
        valid_shift = [
            list(shift)
            for shift in circular_shifts(invalid_sequence, -1)
            if validate_printing_order(prec_dict, succ_dict, shift)[0]
        ][0]
        valid_list.append(valid_shift.pop(0))
        invalid_sequence = valid_shift
    return valid_list


def solve_level2(filename: str):
    input_formatted, succ_dict, prec_dict = get_input_and_rules_dicts(filename)
    invalid_orders = [
        order
        for order in input_formatted
        if not all(validate_printing_order(prec_dict, succ_dict, order))
    ]
    fixed_sequences = [
        fix_sequence(seq, prec_dict, succ_dict) for seq in invalid_orders
    ]
    return calculate_middle_item_sum(fixed_sequences)


if __name__ == "__main__":

    current_directory = os.path.dirname(__file__)

    sample_file = f"{current_directory}/sample1.txt"
    filename1 = f"{current_directory}/input1.txt"
    filename2 = f"{current_directory}/input2.txt"

    get_input_if_not_exists(2024, current_directory, 1)
    print(solve_level1(filename1))
    get_input_if_not_exists(2024, current_directory, 2)
    print(solve_level2(filename2))
