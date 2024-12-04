import os.path
from typing import List, Tuple
import dotenv

from utils.utils import get_input_if_not_exists, read_input_lines

dotenv.load_dotenv()


## Implementation of PART 1


def solve_level1(filename: str):
    lines = read_input_lines(filename)

    result = 1

    return result


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
    get_input_if_not_exists(2024, current_directory, 2)
    print(solve_level2(filename2))
