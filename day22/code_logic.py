from collections import defaultdict
import math
import os.path
from typing import List, Tuple
import dotenv
from tqdm import tqdm

from utils.utils import get_input_if_not_exists, read_input_lines

dotenv.load_dotenv()


## Implementation of PART 1


class SecretNumberGenerator:
    prunning_divisor = 16_777_216

    def __init__(self, initial_number: int):
        self.secret_number = initial_number

    def _mix_with_secret_nb(self, number: int):
        self.secret_number = self.secret_number ^ number

    def _prune_secret_nb(self):
        self.secret_number %= self.prunning_divisor

    def mix_and_prune(self, number: int):
        self._mix_with_secret_nb(number)
        self._prune_secret_nb()

    def generate_new_secret_number(self):
        # Step 1
        step1_nb = self.secret_number * 64
        self.mix_and_prune(step1_nb)

        # Step 2
        step2_nb = math.floor(self.secret_number / 32)
        self.mix_and_prune(step2_nb)

        # Step 3
        step3_nb = self.secret_number * 2048
        self.mix_and_prune(step3_nb)


def solve_level1(filename: str):
    lines = read_input_lines(filename)
    result = 0
    for initial_number in tqdm(lines):
        secret_nb_generator = SecretNumberGenerator(int(initial_number))
        for _ in range(2000):
            secret_nb_generator.generate_new_secret_number()
        result += secret_nb_generator.secret_number
    return result


## Implementation of PART 2
class PriceGenerator(SecretNumberGenerator):
    def __init__(self, initial_number: int):
        super().__init__(initial_number)

    @property
    def price(self):
        return self.secret_number % 10


def get_price_sequence(
    price_generator: PriceGenerator, nb_iterations: int
) -> List[int]:
    price_sequence = []
    for _ in range(nb_iterations):
        price_generator.generate_new_secret_number()
        price_sequence.append(price_generator.price)
    return price_sequence


def get_price_delta_sequence(price_sequence: List[int]) -> List[int]:
    return [
        price_sequence[idx] - price_sequence[idx - 1]
        for idx in range(1, len(price_sequence))
    ]


def solve_level2(filename: str):
    lines = read_input_lines(filename)
    sequence_to_bananas = defaultdict(lambda: 0)
    for initial_number in tqdm(lines):
        price_generator = PriceGenerator(int(initial_number))
        price_sequence = get_price_sequence(price_generator, 2000)
        price_delta_sequence = get_price_delta_sequence(price_sequence)

        assigned_sequences = set()
        for idx in range(4, len(price_delta_sequence) + 1):
            sequence = tuple(price_delta_sequence[idx - 4 : idx])
            if sequence in assigned_sequences:
                continue
            sequence_to_bananas[sequence] += price_sequence[idx]
            assigned_sequences.add(sequence)
    return max(sequence_to_bananas.values())


if __name__ == "__main__":

    current_directory = os.path.dirname(__file__)

    sample_file = f"{current_directory}/sample1.txt"
    sample_file2 = f"{current_directory}/sample2.txt"
    filename1 = f"{current_directory}/input1.txt"
    filename2 = f"{current_directory}/input2.txt"

    # get_input_if_not_exists(2024, current_directory, 1)
    # print(solve_level1(filename1))
    get_input_if_not_exists(2024, current_directory, 2)
    print(solve_level2(filename2))
