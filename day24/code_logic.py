from itertools import zip_longest
import os.path
from typing import Dict, List, Tuple
import dotenv

from utils.utils import get_input_if_not_exists, read_input_lines

dotenv.load_dotenv()


## Implementation of PART 1


def split_input_lines(lines: List[str]) -> Tuple[List[str], List[str]]:
    split_idx = [idx for idx, line in enumerate(lines) if line == ""][0]
    return lines[:split_idx], lines[split_idx + 1 :]


def parse_input_values(input_values: List[str]) -> Dict[str, int]:
    return {line.split(": ")[0]: int(line.split(": ")[1]) for line in input_values}


def parse_operations(operations: List[str]) -> Dict[str, Tuple[str]]:
    result_to_operation_dict = dict()
    for op in operations:
        operation, result = op.split(" -> ")
        operation_tuple = tuple(operation.split(" "))
        result_to_operation_dict[result] = operation_tuple
    return result_to_operation_dict


def solve_logic_system(input_values_dict, operation_to_result_var):
    while len(set(operation_to_result_var.keys()) - set(input_values_dict.keys())) > 0:
        for result_var, operation_tuple in operation_to_result_var.items():
            if all(
                [
                    operation_tuple[0] in input_values_dict,
                    operation_tuple[2] in input_values_dict,
                    result_var not in input_values_dict,
                ]
            ):
                if operation_tuple[1] == "AND":
                    input_values_dict[result_var] = (
                        input_values_dict[operation_tuple[0]]
                        & input_values_dict[operation_tuple[2]]
                    )
                elif operation_tuple[1] == "OR":
                    input_values_dict[result_var] = (
                        input_values_dict[operation_tuple[0]]
                        | input_values_dict[operation_tuple[2]]
                    )
                elif operation_tuple[1] == "XOR":
                    input_values_dict[result_var] = (
                        input_values_dict[operation_tuple[0]]
                        ^ input_values_dict[operation_tuple[2]]
                    )


def solve_level1(filename: str):
    lines = read_input_lines(filename)
    input_values, operations = split_input_lines(lines)
    input_values_dict = parse_input_values(input_values)
    operation_to_result_var = parse_operations(operations)
    solve_logic_system(input_values_dict, operation_to_result_var)
    wires_by_z = sorted(
        [var_name for var_name in input_values_dict if var_name.startswith("z")],
        reverse=True,
    )
    return int(
        "".join([str(input_values_dict[var_name]) for var_name in wires_by_z]), 2
    )


## Implementation of PART 2
# The circuit to add binary numbers is a full adder (apparently arranged as ripple carry adder, from wikipedia)
# We just need to find the faulty wires not really the sitches to make :)
# Loved this https://en.wikipedia.org/wiki/Adder_(electronics)#/media/File:Fulladder.gif


def extract_faulty_z_wires(result_var_to_operations: Dict[str, Tuple[str]]):
    # A full adder needs an XOR as last gate ut for the last one
    for result, operation_tuple in result_var_to_operations.items():
        if all(
            [
                operation_tuple[1] != "XOR",
                result.startswith("z"),
                result != max(result_var_to_operations),
            ]
        ):
            yield result


def extract_wrong_XOR_operations(
    result_var_to_operations: Dict[str, Tuple[str]], input_values_dict: Dict[str, int]
):
    # AXOR always gets input wires x, y) or output wire (z)
    for result, operation_tuple in result_var_to_operations.items():
        if all(
            [
                operation_tuple[1] == "XOR",
                not result.startswith("z"),
                operation_tuple[0] not in input_values_dict,
                operation_tuple[2] not in input_values_dict,
            ]
        ):
            yield result


def extract_wrong_and_operations(
    result_var_to_operations: Dict[str, Tuple[str]], input_values_dict: Dict[str, int]
):
    for result, operation_tuple in result_var_to_operations.items():
        if operation_tuple[1] == "AND":
            # Missing this: First one can be half adder
            if "x00" in operation_tuple:
                continue
            for operation in result_var_to_operations.values():
                if result in operation and operation[1] != "OR":
                    yield result


def extract_faulty_ORs(result_var_to_operations: Dict[str, Tuple[str]]):
    # ORs dont pipe into ORs
    for result, operation_tuple in result_var_to_operations.items():
        if operation_tuple[1] != "OR":
            continue
        for operation in result_var_to_operations.values():
            if result in operation and operation[1] == "OR":
                yield result


def extract_faulty_XORs_by_piping(result_var_to_operations: Dict[str, Tuple[str]]):
    # XORs dont pipe into ORs
    for result, operation_tuple in result_var_to_operations.items():
        if operation_tuple[1] != "XOR":
            continue
        for operation in result_var_to_operations.values():
            if result in operation and operation[1] == "OR":
                yield result


def solve_level2(filename: str):
    lines = read_input_lines(filename)
    input_values, operations = split_input_lines(lines)
    input_values_dict = parse_input_values(input_values)
    result_var_to_operations = parse_operations(operations)
    faulty_z_wires = set(extract_faulty_z_wires(result_var_to_operations))
    wrong_XOR_operations = set(
        extract_wrong_XOR_operations(result_var_to_operations, input_values_dict)
    )
    wrong_AND_operations = set(
        extract_wrong_and_operations(result_var_to_operations, input_values_dict)
    )
    wrong_OR_operations = set(extract_faulty_ORs(result_var_to_operations))
    wrong_XOR_piping = set(extract_faulty_XORs_by_piping(result_var_to_operations))
    return ",".join(
        sorted(
            faulty_z_wires
            | wrong_XOR_operations
            | wrong_AND_operations
            | wrong_OR_operations
            | wrong_XOR_piping
        )
    )


if __name__ == "__main__":

    current_directory = os.path.dirname(__file__)

    sample_file = f"{current_directory}/sample1.txt"
    filename1 = f"{current_directory}/input1.txt"
    filename2 = f"{current_directory}/input2.txt"

    # get_input_if_not_exists(2024, current_directory, 1)
    # print(solve_level1(filename1))
    get_input_if_not_exists(2024, current_directory, 2)
    print(solve_level2(filename2))
