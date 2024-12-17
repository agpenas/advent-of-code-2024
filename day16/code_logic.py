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
class PrunableMaze(Maze):
    def __init__(self, array):
        super().__init__(array)

    def coalesce_max_exploring_leaving_cost(self):
        self.coalesced_mapping = dict()
        for j, row in enumerate(self.array):
            for i, char in enumerate(row):
                if (i, j) in self.walls_set.union({self.start_coords, self.end_coords}):
                    continue
                self.coalesced_mapping[(i, j)] = max(
                    [
                        self.exploring_cost_mapping.get((i, j), -1),
                        self.leaving_cost_mapping.get((i, j), -1),
                    ]
                )

    def print_coalesced_grid(self, cell_length=5):
        self.print_grid(self.coalesced_mapping, cell_length)

    def try_to_prune_grid(self):
        nb_changes_made = 0
        for j, row in enumerate(self.array):
            for i, _ in enumerate(row):
                if (i, j) in self.walls_set.union({self.start_coords, self.end_coords}):
                    continue
                if not self.coalesced_mapping.get((i, j)):
                    continue

                neigh_costs = list()
                for offset in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                    neigh_costs.append(
                        self.coalesced_mapping.get((i + offset[0], j + offset[1]), None)
                    )

                not_none_neigh_costs = [x for x in neigh_costs if x is not None]

                if not not_none_neigh_costs:
                    self.delete_coalesced_cost((i, j))
                    nb_changes_made = True
                    continue
                if (
                    max(not_none_neigh_costs)
                    > self.coalesced_mapping.get((i, j))
                    >= min(not_none_neigh_costs)
                ):
                    continue
                self.delete_coalesced_cost((i, j))
                nb_changes_made += 1
        return nb_changes_made

    def delete_coalesced_cost(self, position):
        self.coalesced_mapping[position] = None

    def launch_coalesced_map_prunning(self):
        self.coalesced_mapping[self.end_coords] = self.get_cost_to_end() + 1
        self.coalesced_mapping[self.start_coords] = 0
        while self.try_to_prune_grid():
            print(self.get_path_length())
            pass

    def get_path_length(self):
        return sum([1 for x in self.coalesced_mapping.values() if x]) + 1


def solve_level2(filename: str):
    lines = read_input_lines(filename)
    array = [[char for char in line] for line in lines]
    maze = PrunableMaze(array)
    maze.explore_grid()
    # maze.print_exploring_grid()
    # maze.print_leaving_grid()
    maze.coalesce_max_exploring_leaving_cost()
    # maze.print_coalesced_grid()
    maze.launch_coalesced_map_prunning()
    maze.print_coalesced_grid()
    return maze.get_path_length()


if __name__ == "__main__":

    current_directory = os.path.dirname(__file__)

    sample_file = f"{current_directory}/sample1.txt"
    sample_file2 = f"{current_directory}/sample2.txt"

    filename1 = f"{current_directory}/input1.txt"
    filename2 = f"{current_directory}/input2.txt"

    # get_input_if_not_exists(2024, current_directory, 1)
    # print(solve_level1(sample_file))
    get_input_if_not_exists(2024, current_directory, 2)
    print(solve_level2(sample_file))
