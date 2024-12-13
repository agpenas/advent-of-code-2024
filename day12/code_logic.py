import os.path
from collections import defaultdict
from typing import Dict, List, Set, Tuple

import dotenv
from utils.utils import get_input_if_not_exists, read_input_lines

dotenv.load_dotenv()


## Implementation of PART 1


def assign_regions_to_array(array: List[List[str]]):
    coords_to_region = dict()
    for row_idx, row in enumerate(array):
        for col_idx, item in enumerate(row):
            if row_idx == 0 or col_idx == 0:
                if row_idx == 0 and col_idx == 0:
                    coords_to_region[(row_idx, col_idx)] = 1
                elif row_idx == 0 and array[row_idx][col_idx - 1] == item:
                    coords_to_region[(0, col_idx)] = coords_to_region[(0, col_idx - 1)]
                elif col_idx == 0 and array[row_idx - 1][col_idx] == item:
                    coords_to_region[(row_idx, 0)] = coords_to_region[(row_idx - 1, 0)]
                else:
                    coords_to_region[(row_idx, col_idx)] = max(coords_to_region.values()) + 1
                continue

            elif array[row_idx - 1][col_idx] == item:
                coords_to_region[(row_idx, col_idx)] = coords_to_region[(row_idx - 1, col_idx)]
            elif array[row_idx][col_idx - 1] == item:
                coords_to_region[(row_idx, col_idx)] = coords_to_region[(row_idx, col_idx - 1)]
            else:
                coords_to_region[(row_idx, col_idx)] = max(coords_to_region.values()) + 1
    return coords_to_region


def inverse_coords_to_region(coords_to_region: Dict[Tuple[int, int], int]) -> Dict[int, Set[Tuple[int, int]]]:
    region_to_coords = defaultdict(set)
    for coord, region in coords_to_region.items():
        region_to_coords[region].add(coord)
    return region_to_coords


def get_region_area(coords_set: Set[Tuple[int, int]]) -> int:
    return len(coords_set)


def get_regions_perimeter(coords_set: Set[Tuple[int, int]]) -> int:
    perimeter = 0
    adjacent_positions = set()
    for coords in coords_set:
        adjacent_positions.add(
            (coords[0] + offset, coords[1] + offset) for offset in [(0, 1), (0, -1), (1, 0), (-1, 0)]
        )
    return len(adjacent_positions - coords_set)


def get_array(lines: List[str]) -> List[List[str]]:
    array = []
    for line in lines:
        array.append(list(line))
    return array


def solve_level1(filename: str):
    lines = read_input_lines(filename)
    array = get_array(lines)
    coords_to_region = assign_regions_to_array(array)
    region_to_coords = inverse_coords_to_region(coords_to_region)
    price = 0
    for region, coords in region_to_coords.items():
        price += get_region_area(coords) * get_regions_perimeter(coords)

    return price


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

    # get_input_if_not_exists(2024, current_directory, 1)
    print(solve_level1(sample_file))
    # get_input_if_not_exists(2024, current_directory, 2)
    # print(solve_level2(filename2))
