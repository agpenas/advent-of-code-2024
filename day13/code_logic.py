import os.path
import re
from typing import List, Tuple

import dotenv
from utils.utils import get_input_if_not_exists, read_input_lines

dotenv.load_dotenv()


## Implementation of PART 1


def solve_equation_system(prize_X, prize_Y, coef_X_A, coef_Y_A, coef_X_B, coef_Y_B):
    # prize_X = coef_X_A * a + coef_X_B * b
    # prize_Y = coef_Y_A * a + coef_Y_B * b
    b = (prize_Y * coef_X_A - prize_X * coef_Y_A) / (coef_X_A * coef_Y_B - coef_Y_A * coef_X_B)
    a = (prize_X - coef_X_B * b) / coef_X_A
    return a, b


def extract_equation_input(line: List[str], increase_prize_dists: bool = False):
    coef_X_A, coef_Y_A = re.findall(r"(\d+)", line[0])
    coef_X_B, coef_Y_B = re.findall(r"(\d+)", line[1])
    prize_X, prize_Y = re.findall(r"(\d+)", line[2])
    extra_distance = 10_000_000_000_000 if increase_prize_dists else 0
    return (
        int(prize_X) + extra_distance,
        int(prize_Y) + extra_distance,
        int(coef_X_A),
        int(coef_Y_A),
        int(coef_X_B),
        int(coef_Y_B),
    )


def get_tokes(A_times, B_times):
    return int(A_times * 3 + B_times)


def solve_level1(filename: str):
    lines = read_input_lines(filename)
    eqs: List[List[str]] = [lines[idx : idx + 3] for idx in range(0, len(lines), 4)]
    result = 0

    for eq in eqs:

        args = extract_equation_input(eq)
        A_times, B_times = solve_equation_system(*args)

        if not A_times.is_integer() or not B_times.is_integer():
            continue

        result += get_tokes(A_times, B_times)

    return result


## Implementation of PART 2


def solve_level2(filename: str):
    lines = read_input_lines(filename)
    eqs: List[List[str]] = [lines[idx : idx + 3] for idx in range(0, len(lines), 4)]
    result = 0
    for eq in eqs:
        args = extract_equation_input(eq, increase_prize_dists=True)
        A_times, B_times = solve_equation_system(*args)
        if any(
            [
                not A_times.is_integer(),
                not B_times.is_integer(),
            ]
        ):
            continue

        result += get_tokes(A_times, B_times)

    return result


if __name__ == "__main__":

    current_directory = os.path.dirname(__file__)

    sample_file = f"{current_directory}/sample1.txt"
    filename1 = f"{current_directory}/input1.txt"
    filename2 = f"{current_directory}/input1.txt"

    get_input_if_not_exists(2024, current_directory, 1)
    print(solve_level1(filename2))
    get_input_if_not_exists(2024, current_directory, 1)
    print(solve_level2(filename2))
