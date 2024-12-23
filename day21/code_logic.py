from collections import Counter, deque
from itertools import chain, combinations, pairwise, permutations, product
import os.path
from typing import Dict, List, Set, Tuple
import dotenv
from tqdm import tqdm

from utils.utils import get_input_if_not_exists, read_input_lines

dotenv.load_dotenv()


## Implementation of PART 1
door_keypad = [
    ["7", "8", "9"],
    ["4", "5", "6"],
    ["1", "2", "3"],
    ["", "0", "A"],
]

robot_keypad = [
    ["", "^", "A"],
    ["<", "v", ">"],
]


class Robot:
    offset_to_char = {
        (0, 1): "v",
        (0, -1): "^",
        (1, 0): ">",
        (-1, 0): "<",
    }

    def __init__(
        self,
        button_to_position_mapping: Dict[str, Tuple[int, int]],
        forbidden_positions: Set[Tuple[int, int]],
        inital_button: str = "A",
    ):
        self.button_to_position = button_to_position_mapping
        self.forbidden_positions = forbidden_positions
        self.current_position = self.button_to_position[inital_button]

    @classmethod
    def from_list_of_lists(
        cls, list_of_lists: List[List[str]], initial_button: str = "A"
    ):
        button_to_position_mapping = dict()
        forbidden_positions = set()
        for j, row in enumerate(list_of_lists):
            for i, char in enumerate(row):
                if char == "":
                    forbidden_positions.add((i, j))
                    continue
                button_to_position_mapping[char] = (i, j)
        return cls(button_to_position_mapping, forbidden_positions, initial_button)

    def get_offset_to_next_button(self, next_button: str) -> Tuple[int, int]:
        next_position = self.button_to_position[next_button]
        return (
            next_position[0] - self.current_position[0],
            next_position[1] - self.current_position[1],
        )

    def decompose_offset_in_tuples(
        self, offset: Tuple[int, int]
    ) -> List[Tuple[int, int]]:
        list_of_tuples = list()
        if offset[0] != 0:
            list_of_tuples.extend(
                [(1 - 2 * int(offset[0] < 0), 0) for _ in range(abs(offset[0]))]
            )
        if offset[1] != 0:
            list_of_tuples.extend(
                [(0, 1 - 2 * int(offset[1] < 0)) for _ in range(abs(offset[1]))]
            )
        return list_of_tuples

    def get_tuple_combinations(
        self, list_of_tuples: List[Tuple[int, int]]
    ) -> List[Tuple[Tuple[int, int]]]:
        return set(permutations(list_of_tuples, len(list_of_tuples)))

    def _get_intermediary_positions(
        self, list_of_tuples: List[Tuple[int, int]]
    ) -> List[Tuple[int, int]]:
        intermediary_positions = list()
        prev_pos = self.current_position
        for tupl in list_of_tuples:
            intermediary_positions.append(
                (prev_pos[0] + tupl[0], prev_pos[1] + tupl[1])
            )
            prev_pos = intermediary_positions[-1]
        return intermediary_positions

    def validate_tuple_combinations(
        self, tuple_combinations: List[Tuple[Tuple[int, int]]]
    ) -> List[Tuple[Tuple[int, int]]]:
        valid_combinations = list()
        for tuple_combo in tuple_combinations:
            intermediary_positions = self._get_intermediary_positions(tuple_combo)
            if any([pos in self.forbidden_positions for pos in intermediary_positions]):
                continue
            valid_combinations.append(tuple_combo)
        return valid_combinations

    def translate_tuples_into_chars_and_add_A(
        self, tuple_combinations: List[Tuple[Tuple[int, int]]]
    ) -> List[str]:
        return [
            "".join([self.offset_to_char[tupl] for tupl in combo]) + "A"
            for combo in tuple_combinations
        ]

    def _get_nb_button_transitions(self, sequence: Tuple[Tuple[int, int]]) -> int:
        return sum(
            [sequence[idx - 1] != sequence[idx] for idx in range(1, len(sequence))]
        )

    def get_sequences_with_lowest_button_transitions(
        self, sequences: List[Tuple[Tuple[int, int]]]
    ) -> List[Tuple[Tuple[int, int]]]:
        nb_transitions = [
            self._get_nb_button_transitions(sequence) for sequence in sequences
        ]
        min_transitions = min(nb_transitions)
        return [
            sequence
            for idx, sequence in enumerate(sequences)
            if nb_transitions[idx] == min_transitions
        ]

    def get_possible_move_combos_to_button(self, next_button: str) -> List[str]:
        offset = self.get_offset_to_next_button(next_button)
        list_of_tuples = self.decompose_offset_in_tuples(offset)
        tuple_combinations = self.get_tuple_combinations(list_of_tuples)
        valid_combinations = self.validate_tuple_combinations(tuple_combinations)
        efficient_combinations = self.get_sequences_with_lowest_button_transitions(
            valid_combinations
        )
        return self.translate_tuples_into_chars_and_add_A(efficient_combinations)

    def get_possible_move_combos_for_sequence(self, sequence: str) -> List[str]:
        moves_list = list()
        for button in sequence:
            moves_list.append(self.get_possible_move_combos_to_button(button))
            self.current_position = self.button_to_position[button]
        return ["".join(seq_combo) for seq_combo in list(product(*moves_list))]


def solve_level1(filename: str):
    lines = read_input_lines(filename)

    door_robot = Robot.from_list_of_lists(door_keypad)
    radiation_robot = Robot.from_list_of_lists(robot_keypad)
    freezing_robot = Robot.from_list_of_lists(robot_keypad)

    code_complexities = list()
    for sequence in lines:
        door_bot_moves = door_robot.get_possible_move_combos_for_sequence(sequence)
        radiation_bot_moves = list(
            chain.from_iterable(
                [
                    radiation_robot.get_possible_move_combos_for_sequence(
                        door_bot_move_sequence
                    )
                    for door_bot_move_sequence in door_bot_moves
                ]
            )
        )

        freezing_bot_moves = list(
            chain.from_iterable(
                [
                    freezing_robot.get_possible_move_combos_for_sequence(
                        radiation_bot_move_sequence
                    )
                    for radiation_bot_move_sequence in radiation_bot_moves
                ]
            )
        )
        min_nb_buttons = min(map(len, freezing_bot_moves))
        print(door_bot_moves)
        print(
            radiation_bot_moves[:1],
        )
        print(freezing_bot_moves[:1])
        int_in_sequence = int(sequence.strip("A"))
        code_complexities.append(min_nb_buttons * int_in_sequence)

    result = sum(code_complexities)

    return result


## Implementation of PART 2
# Let's make a dict of optinmal moves for each button transition


def forecast_min_nb_buttons_for_n_robots(sequence: str, n_robots: int) -> int:
    robot_list = [Robot.from_list_of_lists(robot_keypad) for _ in range(n_robots)]
    sequences = [sequence]
    for robot in robot_list:
        sequences = set(
            chain.from_iterable(
                robot.get_possible_move_combos_for_sequence(sequence)
                for sequence in sequences
            )
        )
    return min(map(len, sequences))


def get_best_sequence(sequences: List[str]):
    if len(sequences) == 1:
        return sequences[0]

    for nb_robots in range(1, 5):
        nb_buttons = [
            forecast_min_nb_buttons_for_n_robots(seq, nb_robots) for seq in sequences
        ]
        if len(set(nb_buttons)) > 1:
            break
    if len(set(nb_buttons)) == 1:
        raise ValueError("All sequences have the same number of buttons")

    return [seq for seq, nb in zip(sequences, nb_buttons) if nb == min(nb_buttons)][0]


def get_transition_cache():
    numeric_keypad_transitions = list(map("".join, product("0123456789A", repeat=2)))
    robot_keypad_transitions = list(map("".join, product("<>^vA", repeat=2)))
    transitions_mapping = dict()

    for transition in robot_keypad_transitions:
        robot_robot = Robot.from_list_of_lists(
            robot_keypad, initial_button=transition[0]
        )
        robot_robot_seqs = robot_robot.get_possible_move_combos_for_sequence(
            transition[1]
        )
        transitions_mapping[transition] = get_best_sequence(robot_robot_seqs)

    for transition in numeric_keypad_transitions:
        door_robot = Robot.from_list_of_lists(door_keypad, initial_button=transition[0])
        door_robot_seqs = door_robot.get_possible_move_combos_for_sequence(
            transition[1]
        )
        transitions_mapping[transition] = get_best_sequence(door_robot_seqs)

    return transitions_mapping


def get_sequence_after_n_iters(
    sequence: str,
    n_iters: int,
    cache: Dict[str, str],
    pad_with_preceeding_A: bool = True,
) -> str:
    for i in range(n_iters):
        new_sequence = deque()
        sequence = "A" + sequence if pad_with_preceeding_A and i > 0 else sequence

        for transition in pairwise(sequence):
            new_sequence.append(cache["".join(transition)])
        sequence = "".join(new_sequence)
    return sequence


def solve_level2(filename: str):
    lines = read_input_lines(filename)
    transition_cache = get_transition_cache()
    code_complexities = list()
    for initial_sequence in lines:
        final_len = 0
        sequence = get_sequence_after_n_iters(
            "A" + initial_sequence, 13, transition_cache
        )
        for transition, counts in Counter(pairwise(sequence)).items():
            extra_len = (
                len(
                    get_sequence_after_n_iters(
                        "".join(transition),
                        13,
                        transition_cache,
                        pad_with_preceeding_A=True,
                    )
                )
                * counts
            )

            final_len += extra_len
        final_len += len(
            get_sequence_after_n_iters("A" + sequence[0], 13, transition_cache)
        )
        int_in_sequence = int(initial_sequence.strip("A"))
        code_complexities.append(final_len * int_in_sequence)
    return sum(code_complexities)


if __name__ == "__main__":

    current_directory = os.path.dirname(__file__)

    sample_file = f"{current_directory}/sample1.txt"
    filename1 = f"{current_directory}/input1.txt"
    filename2 = f"{current_directory}/input2.txt"

    # get_input_if_not_exists(2024, current_directory, 1)
    # print(solve_level1(sample_file))
    get_input_if_not_exists(2024, current_directory, 2)
    print(solve_level2(filename1))
