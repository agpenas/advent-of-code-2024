import os.path
import re
from typing import List, Tuple

import dotenv
from tqdm import tqdm
from utils.utils import get_input_if_not_exists, read_input_lines

dotenv.load_dotenv()


## Implementation of PART 1


class Grid:
    def __init__(self, max_x, max_y, fallen_bytes) -> None:
        self.max_x = max_x
        self.max_y = max_y
        self.fallen_bytes = fallen_bytes
        self.initial_position = (0, 0)
        self.end_position = (max_x - 1, max_y - 1)
        self.positions_to_explore = [(0, 0)]
        self.position_to_cost = {self.initial_position: 0}

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
            if new_position in self.fallen_bytes:
                continue
            if not 0 <= new_position[0] < self.max_x or not 0 <= new_position[1] < self.max_y:
                continue
            if self.position_to_cost.get(new_position, 100_000_000) > self.position_to_cost[position] + 1:
                possible_moves.append(new_position)
        return possible_moves

    def explore_grid(self):
        while self.positions_to_explore:
            current_position = self.positions_to_explore.pop(0)
            if current_position == self.end_position:
                return True
            possible_moves_list = self.get_posssible_moves(current_position)
            if not possible_moves_list:
                continue
            self.positions_to_explore.extend(possible_moves_list)
            for move in possible_moves_list:
                self.position_to_cost[move] = self.position_to_cost[current_position] + 1
            # self.print_grid()
            # print("----")
        return False

    def get_shortest_path(self):
        self.explore_grid()
        return self.position_to_cost[self.end_position]

    def exists_path_to_exit(self):
        return self.explore_grid()


def solve_level1(filename: str, max_x, max_y, input_nb_lines):
    lines = read_input_lines(filename)
    lines_to_use = lines[:input_nb_lines]
    coords = {tuple(map(int, re.findall(r"(\d+)", line))) for line in lines_to_use}
    grid = Grid(max_x=max_x, max_y=max_y, fallen_bytes=coords)
    result = grid.get_shortest_path()

    return result


## Implementation of PART 2


def solve_level2(filename: str, max_x, max_y):
    lines = read_input_lines(filename)
    for nb_lines in tqdm(range(len(lines))):
        lines_to_use = lines[:nb_lines]
        coords = {tuple(map(int, re.findall(r"(\d+)", line))) for line in lines_to_use}
        grid = Grid(max_x=max_x, max_y=max_y, fallen_bytes=coords)
        if not grid.exists_path_to_exit():
            return lines_to_use[nb_lines - 1]
    raise ValueError("No solution found")


if __name__ == "__main__":

    current_directory = os.path.dirname(__file__)

    sample_file = f"{current_directory}/sample1.txt"
    filename1 = f"{current_directory}/input1.txt"

    # get_input_if_not_exists(2024, current_directory, 1)
    print(solve_level1(sample_file, 7, 7))
    # print(solve_level2(filename1))
