import os.path
from typing import Dict, List, Tuple
import dotenv

from utils.utils import get_input_if_not_exists, read_input_lines

dotenv.load_dotenv()


## Implementation of PART 1


def split_input_lines(lines: List[str]) -> Tuple[List[str], List[str]]:
    split_idx = [idx for idx, line in enumerate(lines) if line == ""][0]
    return lines[:split_idx], lines[split_idx + 1 :]


class Instruction:
    def __init__(self, opcode: int, operand: int, register: Dict[str, int]):
        self.opcode = opcode
        self.operand = operand
        self.register = register
        self.instruction_pointer = None

    @property
    def combo_operand(self):
        if self.operand <= 3:
            return self.operand
        elif self.operand == 7:
            raise ValueError("Operand cannot be 7")
        else:
            return self.register["ABC"[self.operand - 4]]

    def run(self, output):
        match self.opcode:
            case 0:
                self.register["A"] = int(self.register["A"] / 2**self.combo_operand)
            case 1:
                self.register["B"] = self.operand ^ self.register["B"]
            case 2:
                self.register["B"] = self.combo_operand % 8
            case 3:
                if self.register["A"] > 0:
                    self.instruction_pointer = self.operand
            case 4:
                self.register["B"] = self.register["B"] ^ self.register["C"]
            case 5:
                output.append(self.combo_operand % 8)
            case 6:
                self.register["B"] = int(self.register["A"] / 2**self.combo_operand)
            case 7:
                self.register["C"] = int(self.register["A"] / 2**self.combo_operand)


def solve_level1(filename: str):
    lines = read_input_lines(filename)
    register_input, program_input = split_input_lines(lines)
    register = {
        letter: int(line.split(": ")[1]) for letter, line in zip("ABC", register_input)
    }
    program_opcodes = [int(val) for val in program_input[0].split(": ")[1].split(",")]
    output = run_program(register, program_opcodes)
    return ",".join(map(str, output))


def run_program(register, program_opcodes):
    instruction_idx = 0
    output = list()
    while True:
        if instruction_idx >= len(program_opcodes):
            break
        opcode, operand = list(zip(program_opcodes[:-1], program_opcodes[1:]))[
            instruction_idx
        ]
        instruction = Instruction(opcode, operand, register)
        instruction.run(output)
        instruction_idx = (
            instruction.instruction_pointer
            if instruction.instruction_pointer is not None
            else instruction_idx + 2
        )

    return output


## Implementation of PART 2


def search_input_a_value(register, program_opcodes, min_value=None, current_idx=None):

    min_value = min_value if min_value else 8 ** (len(program_opcodes) - 1)
    new_min_value = None

    for idx, target_value in enumerate(program_opcodes[::-1]):

        idx = len(program_opcodes) - idx - 1

        if current_idx:
            if idx >= current_idx:
                continue

        for j in range(9):
            min_value = new_min_value if new_min_value else min_value
            initial_register_value = min_value + 8 ** (idx) * j

            register["A"] = initial_register_value
            output = run_program(register, program_opcodes)

            if "".join(map(str, output)) == "".join(map(str, program_opcodes)):
                return initial_register_value

            if output[idx] == target_value:

                new_min_value = search_input_a_value(
                    register, program_opcodes, initial_register_value, idx
                )
                if not new_min_value:
                    continue

                else:
                    return new_min_value
        if j > 7:
            return


def solve_level2(filename: str):
    lines = read_input_lines(filename)
    register_input, program_input = split_input_lines(lines)
    register = {
        letter: int(line.split(": ")[1]) for letter, line in zip("ABC", register_input)
    }
    program_opcodes = [int(val) for val in program_input[0].split(": ")[1].split(",")]
    return search_input_a_value(register, program_opcodes)


if __name__ == "__main__":

    current_directory = os.path.dirname(__file__)

    sample_file = f"{current_directory}/sample1.txt"
    filename1 = f"{current_directory}/input1.txt"
    filename2 = f"{current_directory}/input2.txt"

    # get_input_if_not_exists(2024, current_directory, 1)
    # print(solve_level1(filename1))
    get_input_if_not_exists(2024, current_directory, 2)
    print(solve_level2(filename1))
