from collections import Counter, defaultdict
import copy
from itertools import combinations, permutations
import os.path
from typing import List, Tuple
import dotenv
from tqdm import tqdm

from utils.utils import get_input_if_not_exists, read_input_lines

dotenv.load_dotenv()


## Implementation of PART 1
# Let's reuse some code from day 18 and 16


class Grid:
    vertical_cheat_offsets = [(1, 0), (-1, 0)]
    horizontal_cheat_offsets = [(0, 1), (0, -1)]

    def __init__(self, array) -> None:
        self.array = array
        self.start_coords = self.get_positions_by_character("S")[0]
        self.end_coords = self.get_positions_by_character("E")[0]
        self.walls_set = set(self.get_positions_by_character("#"))
        self.position_to_cost = {self.start_coords: 0}
        self.positions_to_explore = [self.start_coords]

    def get_positions_by_character(self, character):
        coords_list = list()
        for j, row in enumerate(self.array):
            for i, char in enumerate(row):
                if char == character:
                    coords_list.append((i, j))
        return coords_list

    def print_grid(self):
        for y in range(self.max_y):
            for x in range(self.max_x):
                if (x, y) == self.initial_position:
                    print("S", end="")
                elif (x, y) == self.end_position:
                    print("E", end="")
                elif (x, y) in self.fallen_bytes:
                    print("#", end="")
                elif (x, y) in self.position_to_cost:
                    print(self.position_to_cost[(x, y)], end="")
                else:
                    print(".", end="")
            print()

    def get_posssible_moves(self, position):
        possible_moves = []
        for offset in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            new_position = (position[0] + offset[0], position[1] + offset[1])
            if new_position in self.walls_set:
                continue
            if new_position not in self.position_to_cost:
                possible_moves.append(new_position)
        return possible_moves

    def explore_grid(self):
        while self.positions_to_explore:
            current_position = self.positions_to_explore.pop(0)
            if current_position == self.end_coords:
                return
            possible_moves_list = self.get_posssible_moves(current_position)
            if not possible_moves_list:
                continue
            self.positions_to_explore.extend(possible_moves_list)
            for move in possible_moves_list:
                self.position_to_cost[move] = (
                    self.position_to_cost[current_position] + 1
                )
        return

    def get_cheating_dict(self):
        cheat_mapping = dict()
        for wall_coords in self.walls_set:
            # Lets assume no walls are isolated (vertical and horizontal cheats possible)
            # since there is only one path to the end
            for offset_pairs in [
                self.vertical_cheat_offsets,
                self.horizontal_cheat_offsets,
            ]:
                coords1 = (
                    wall_coords[0] + offset_pairs[0][0],
                    wall_coords[1] + offset_pairs[0][1],
                )
                coords2 = (
                    wall_coords[0] + offset_pairs[1][0],
                    wall_coords[1] + offset_pairs[1][1],
                )
                if all(
                    [coords1 in self.position_to_cost, coords2 in self.position_to_cost]
                ):
                    cheat_mapping[(coords1, coords2)] = (
                        abs(
                            self.position_to_cost[coords1]
                            - self.position_to_cost[coords2]
                        )
                        - 2
                    )
        return cheat_mapping


def solve_level1(filename: str, picosecs_gain):
    lines = read_input_lines(filename)
    grid = Grid(lines)
    grid.explore_grid()
    cheat_dict = grid.get_cheating_dict()

    return len(
        [coords for coords, picosecs in cheat_dict.items() if picosecs >= picosecs_gain]
    )


## Implementation of PART 2


# For this question, we can just add up the valid combos start-end
class CheatingGrid(Grid):
    def __init__(self, array) -> None:
        super().__init__(array)

    def get_nb_cheats_with_constraints(self, max_distance=20, picosecs_gain=100):
        if not self.position_to_cost:
            raise ValueError("You need to calculate the path first")
        valid_cheats = 0
        for coord1, coord2 in combinations(self.position_to_cost.keys(), 2):
            distance = abs(coord1[0] - coord2[0]) + abs(coord1[1] - coord2[1])
            if distance > max_distance:
                continue
            if (
                abs(self.position_to_cost[coord2] - self.position_to_cost[coord1])
                - distance
                >= picosecs_gain
            ):
                valid_cheats += 1
        return valid_cheats


def solve_level2(filename: str, picosecs_gain):
    lines = read_input_lines(filename)
    grid = CheatingGrid(lines)
    grid.explore_grid()
    return grid.get_nb_cheats_with_constraints(20, picosecs_gain)


if __name__ == "__main__":

    current_directory = os.path.dirname(__file__)

    sample_file = f"{current_directory}/sample1.txt"
    filename1 = f"{current_directory}/input1.txt"
    filename2 = f"{current_directory}/input2.txt"

    # get_input_if_not_exists(2024, current_directory, 1)
    # print(solve_level1(filename1))
    get_input_if_not_exists(2024, current_directory, 2)
    print(solve_level2(sample_file, 50))
