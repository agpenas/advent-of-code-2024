import os.path
from typing import List, Tuple

import dotenv
from utils.utils import get_input_if_not_exists, read_input_lines

dotenv.load_dotenv()


class HypotheticReindeer:
    def __init__(
        self, position: Tuple[int, int], direction: Tuple[int, int], cum_cost: int
    ) -> None:
        self.direction = direction
        self.position = position
        self.cum_cost = cum_cost


## Implementation of PART 1
class Maze:
    def __init__(self, array):
        self.array = array
        self.start_coords = self.get_positions_by_character("S")[0]
        self.end_coords = self.get_positions_by_character("E")[0]
        self.walls_set = set(self.get_positions_by_character("#"))
        self.exploring_cost_mapping = self.get_cost_mapping()
        self.leaving_cost_mapping = dict()
        self.exploration_queue = [
            (self.start_coords, HypotheticReindeer(self.start_coords, (1, 0), 0))
        ]

    def get_positions_by_character(self, character):
        coords_list = list()
        for j, row in enumerate(self.array):
            for i, char in enumerate(row):
                if char == character:
                    coords_list.append((i, j))
        return coords_list

    def get_cost_mapping(self):
        cost_mapping = dict()
        known_coords = self.walls_set
        for j, row in enumerate(self.array):
            for i, char in enumerate(row):
                if (i, j) in known_coords:
                    continue
                cost_mapping[(i, j)] = 100_000_000
        cost_mapping[self.start_coords] = 0
        return cost_mapping

    def update_position_cost(self, position, cost):
        self.exploring_cost_mapping[position] = cost

    def update_leaving_cost(self, position, cost):
        self.leaving_cost_mapping[position] = min(
            [self.leaving_cost_mapping.get(position, 100_000_000), cost]
        )

    def explore_position(self, exploration_tuple):
        current_pos, reindeer = exploration_tuple
        if current_pos == self.end_coords:
            return

        for offset in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            next_pos = (current_pos[0] + offset[0], current_pos[1] + offset[1])
            step_cost: int = 1 + 1000 * int(offset != reindeer.direction)
            if next_pos in self.walls_set:
                continue
            if (
                self.leaving_cost_mapping.get(next_pos, 100_000_000)
                >= reindeer.cum_cost + step_cost
            ):
                cost = reindeer.cum_cost + step_cost
                self.update_position_cost(next_pos, cost)
                self.update_leaving_cost(current_pos, cost)
                if next_pos == self.end_coords:
                    self.update_leaving_cost(next_pos, cost + step_cost)
                self.exploration_queue.append(
                    (
                        next_pos,
                        HypotheticReindeer(
                            next_pos, offset, self.exploring_cost_mapping.get(next_pos)
                        ),
                    )
                )

    def explore_grid(self):
        while self.exploration_queue:
            exploration_tuple = self.exploration_queue.pop(0)
            self.explore_position(exploration_tuple)

    def get_cost_to_end(self):
        return self.exploring_cost_mapping.get(self.end_coords)

    def print_grid(self, grid, cell_length=5):
        for j, row in enumerate(self.array):
            row_to_print = list()
            for i, char in enumerate(row):
                if char == "#":
                    row_to_print.append("#" * cell_length + " | ")
                    continue
                string_to_append = str(grid.get((i, j)))

                row_to_print.append(
                    string_to_append
                    + (cell_length - len(string_to_append)) * " "
                    + " | "
                )
            print("".join(row_to_print))

    def print_leaving_grid(self, cell_length=5):
        self.print_grid(self.leaving_cost_mapping, cell_length)

    def print_exploring_grid(self, cell_length=5):
        self.print_grid(self.exploring_cost_mapping, cell_length)


def solve_level1(filename: str):
    lines = read_input_lines(filename)
    array = [[char for char in line] for line in lines]
    maze = Maze(array)
    maze.explore_grid()
    maze.print_exploring_grid()
    maze.print_leaving_grid()

    return maze.get_cost_to_end()


## Implementation of PART 2
class BackwardableMaze(Maze):
    def __init__(self, array):
        super().__init__(array)
        self.backwards_exploration_queue = [self.end_coords]
        self.valid_paths_coords = set([self.end_coords])

    def explore_backwards(self):
        self.leaving_cost_mapping[self.end_coords] = (
            self.exploring_cost_mapping.get(self.end_coords) + 1
        )

        while self.backwards_exploration_queue:
            current_pos = self.backwards_exploration_queue.pop(0)
            self.explore_position_backwards(current_pos)

    def explore_position_backwards(self, coords):
        for offset in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            next_pos = (coords[0] + offset[0], coords[1] + offset[1])
            if next_pos in self.walls_set:
                continue
            if self.leaving_cost_mapping.get(
                next_pos, 100_000_000
            ) < self.leaving_cost_mapping.get(coords):
                self.backwards_exploration_queue.append(next_pos)
                self.valid_paths_coords.add(next_pos)


def solve_level2(filename: str):
    lines = read_input_lines(filename)
    array = [[char for char in line] for line in lines]
    maze = BackwardableMaze(array)
    maze.explore_grid()
    maze.explore_backwards()
    # maze.print_exploring_grid()
    # maze.print_leaving_grid()
    return len(maze.valid_paths_coords)


if __name__ == "__main__":

    current_directory = os.path.dirname(__file__)

    sample_file = f"{current_directory}/sample1.txt"
    sample_file2 = f"{current_directory}/sample2.txt"

    filename1 = f"{current_directory}/input1.txt"
    filename2 = f"{current_directory}/input2.txt"

    # get_input_if_not_exists(2024, current_directory, 1)
    # print(solve_level1(sample_file))
    get_input_if_not_exists(2024, current_directory, 2)
    print(solve_level2(filename2))
