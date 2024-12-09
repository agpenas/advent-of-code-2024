from ast import literal_eval
from itertools import chain, product
import os.path
from typing import Dict, List
import dotenv
from tqdm import tqdm

from utils.utils import get_input_if_not_exists, read_input_lines

dotenv.load_dotenv()


## Implementation of PART 1


def get_equation_tuples(lines):
    equations_tuple = [
        (int(result), [fact for fact in factors.split()])
        for line in lines
        for result, factors in [line.split(": ")]
    ]

    return equations_tuple


def generate_binary_combinations(n: int) -> Dict[int, List[List[int]]]:

    def _replace_bin_by_operators(seq: List[int]) -> List[str]:
        return ["*" if bin else "+" for bin in seq]

    binary_list = list(
        chain.from_iterable(
            [product([0, 1], repeat=nb_ops) for nb_ops in range(1, n + 1)]
        )
    )
    sum_value_to_combos = {
        total: [
            _replace_bin_by_operators(seq) for seq in binary_list if sum(seq) == total
        ]
        for total in range(n + 1)
    }
    return sum_value_to_combos


def solve_level1(filename: str):
    lines = read_input_lines(filename)
    equations_tuple = get_equation_tuples(lines)
    sum_value_to_combos = generate_binary_combinations(
        max(len(factors) for _, factors in equations_tuple)
    )
    valid_results = [
        result
        for result, factors in equations_tuple
        if validate_equation(factors, result, sum_value_to_combos)
    ]

    return sum(valid_results)


def write_eq_and_eval(factors, operators, result):
    fact1, remaining_facts = factors[0], factors[1:]
    for op, fact2 in zip(operators, remaining_facts):
        fact1 = eval(str(fact1) + op + fact2)
        if fact1 > result:
            return -1
    return fact1


def validate_equation(factors, result, sum_value_to_combos):
    for nb_mults in range(len(factors), -1, -1):
        are_results_still_higher = False
        for operators in sum_value_to_combos[nb_mults]:
            if len(operators) != len(factors) - 1:
                continue
            eval_result = write_eq_and_eval(factors, operators, result)
            if eval_result == result:
                return True
            if eval_result > result:
                are_results_still_higher = True
        if not are_results_still_higher:
            continue
    return False


## Implementation of PART 2


def generate_binary_combinations_level2(n: int) -> Dict[int, List[List[int]]]:

    binary_list = list(
        chain.from_iterable(
            [product(["*", "+", ""], repeat=nb_ops) for nb_ops in range(1, n + 1)]
        )
    )
    len_to_combos = {
        total: [seq for seq in binary_list if len(seq) == total]
        for total in range(n + 1)
    }
    return len_to_combos


def solve_level2(filename: str):
    lines = read_input_lines(filename)
    equations_tuple = get_equation_tuples(lines)
    len_to_combos = generate_binary_combinations_level2(
        max(len(factors) for _, factors in equations_tuple)
    )
    valid_results = [
        result
        for result, factors in tqdm(equations_tuple)
        if validate_equation_level2(factors, result, len_to_combos)
    ]

    return sum(valid_results)


def validate_equation_level2(factors, result, sum_value_to_combos):

    for operators in sum_value_to_combos[len(factors)]:
        eval_result = write_eq_and_eval(factors, operators, result)
        if eval_result == result:
            return True
    return False


if __name__ == "__main__":

    current_directory = os.path.dirname(__file__)

    sample_file = f"{current_directory}/sample1.txt"
    filename1 = f"{current_directory}/input1.txt"
    filename2 = f"{current_directory}/input2.txt"

    # get_input_if_not_exists(2024, current_directory, 1)
    # print(solve_level1(filename1))
    get_input_if_not_exists(2024, current_directory, 2)
    print(solve_level2(filename2))
