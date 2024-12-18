import os.path
from collections import defaultdict
from itertools import chain, combinations, product
from typing import Dict, List, Tuple

import dotenv
from utils.utils import get_input_if_not_exists, read_input_lines

dotenv.load_dotenv()


## Implementation of PART 1


class AntennasGrid:
    def __init__(self, max_x, max_y, antennas_positions_map: Dict[str, List[Tuple[int, int]]]) -> None:
        self.antennas_positions_map = antennas_positions_map
        self.max_x = max_x
        self.max_y = max_y
        self.frequency_antinodes_map = defaultdict(list)

    @classmethod
    def from_input_lines(cls, lines: List[str]):
        antennas_position_map = defaultdict(list)
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                if char == ".":
                    continue
                antennas_position_map[char].append((x, y))
        max_x = len(lines[0])
        max_y = len(lines)
        return cls(max_x, max_y, antennas_position_map)

    def get_antinodes_for_antennas_pair(
        self, antenna1: Tuple[int, int], antenna2: Tuple[int, int]
    ) -> List[Tuple[int, int]]:
        antenna_dist_x = antenna2[0] - antenna1[0]
        antenna_dist_y = antenna2[1] - antenna1[1]
        antinode1 = antenna2[0] + antenna_dist_x, antenna2[1] + antenna_dist_y
        antinode2 = antenna1[0] - antenna_dist_x, antenna1[1] - antenna_dist_y
        return [antinode1, antinode2]

    def add_antinodes_for_frequency(self, antenna_id: str, antenna_list: List[Tuple[int, int]]):
        for antenna_pair in combinations(antenna_list, r=2):
            self.frequency_antinodes_map[antenna_id].extend(self.get_antinodes_for_antennas_pair(*antenna_pair))

    def add_antinodes_for_all_frequencies(self):
        for antenna_id, antenna_list in self.antennas_positions_map.items():
            self.add_antinodes_for_frequency(antenna_id, antenna_list)

    def filter_antinodes_by_max_dims(self):
        self.frequency_antinodes_map = {
            k: [antinode for antinode in v if 0 <= antinode[0] < self.max_x and 0 <= antinode[1] < self.max_y]
            for k, v in self.frequency_antinodes_map.items()
        }

    def count_unique_antinodes(self):
        return len(set(chain.from_iterable(self.frequency_antinodes_map.values())))


def solve_level1(filename: str):
    lines = read_input_lines(filename)
    antennas_grid = AntennasGrid.from_input_lines(lines)
    antennas_grid.add_antinodes_for_all_frequencies()
    antennas_grid.filter_antinodes_by_max_dims()
    result = antennas_grid.count_unique_antinodes()

    return result


## Implementation of PART 2


class HarmonicAntennaGrid(AntennasGrid):

    def get_antinodes_for_antennas_pair(
        self, antenna1: Tuple[int, int], antenna2: Tuple[int, int]
    ) -> List[Tuple[int, int]]:
        antenna_dist_x = antenna2[0] - antenna1[0]
        antenna_dist_y = antenna2[1] - antenna1[1]
        antinodes = list()
        for antenna, dist_x, dist_y in (
            (antenna2, antenna_dist_x, antenna_dist_y),
            (antenna1, -antenna_dist_x, -antenna_dist_y),
        ):
            for multiplier in range(0, 2000):
                antinode = antenna[0] + dist_x * multiplier, antenna[1] + dist_y * multiplier
                if antinode[0] < 0 or antinode[0] >= self.max_x or antinode[1] < 0 or antinode[1] >= self.max_y:
                    break
                antinodes.append(antinode)
        return antinodes


def solve_level2(filename: str):
    lines = read_input_lines(filename)
    antennas_grid = HarmonicAntennaGrid.from_input_lines(lines)
    antennas_grid.add_antinodes_for_all_frequencies()
    antennas_grid.filter_antinodes_by_max_dims()
    result = antennas_grid.count_unique_antinodes()
    return result


if __name__ == "__main__":

    current_directory = os.path.dirname(__file__)

    sample_file = f"{current_directory}/sample1.txt"
    filename1 = f"{current_directory}/input1.txt"

    # get_input_if_not_exists(2024, current_directory, 1)
    # print(solve_level1(filename1))
    # get_input_if_not_exists(2024, current_directory, 2)
    print(solve_level2(filename1))
