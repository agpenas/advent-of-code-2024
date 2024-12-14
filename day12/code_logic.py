from itertools import chain, product
import os.path
from collections import Counter, defaultdict, deque
from typing import Dict, List, Set, Tuple

import dotenv
from utils.utils import get_input_if_not_exists, read_input_lines

dotenv.load_dotenv()


## Implementation of PART 1


def assign_regions_to_array(array: List[List[str]]):
    coords_to_region_label = {
        coords: idx
        for idx, coords in enumerate(product(range(len(array[0])), range(len(array))))
    }
    coords_to_letter = {
        coords: array[coords[0]][coords[1]]
        for coords in product(range(len(array[0])), range(len(array)))
    }
    offsets = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    is_loop_unconverged = False
    while not is_loop_unconverged:
        is_loop_unconverged = True

        for coords in coords_to_region_label.keys():
            neighs = [(coords[0] + offs[0], coords[1] + offs[1]) for offs in offsets]
            neighs_same_plot = [
                neigh
                for neigh in neighs
                if coords_to_letter.get(neigh, "") == coords_to_letter[coords]
            ]
            group_labels = [
                coords_to_region_label[xy] for xy in [coords] + neighs_same_plot
            ]
            if len(set(group_labels)) == 1:
                continue
            for xy in [coords] + neighs_same_plot:
                coords_to_region_label[xy] = min(group_labels)
            is_loop_unconverged = False
    return coords_to_region_label


def inverse_coords_to_region(
    coords_to_region: Dict[Tuple[int, int], int]
) -> Dict[int, Set[Tuple[int, int]]]:
    region_to_coords = defaultdict(set)
    for coord, region in coords_to_region.items():
        region_to_coords[region].add(coord)
    return region_to_coords


def get_region_area(coords_set: Set[Tuple[int, int]]) -> int:
    return len(coords_set)


def get_regions_perimeter(coords_set: Set[Tuple[int, int]]) -> int:
    adjacent_positions = get_adjacent_positions_counter(coords_set)
    return sum(
        [
            count
            for coords, count in adjacent_positions.items()
            if coords not in coords_set
        ]
    )


def get_adjacent_positions_counter(coords_set):
    adjacent_positions = Counter()
    for coords in coords_set:
        adjacent_positions.update(
            (coords[0] + offset[0], coords[1] + offset[1])
            for offset in [(0, 1), (0, -1), (1, 0), (-1, 0)]
        )

    return adjacent_positions


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
def group_coords_by_straight_lines(
    adj_set: Set[Tuple[int, int]], coords_set: Set[Tuple[int, int]]
) -> int:

    def _are_sides_in_coords(
        coord_tup: Tuple[int, int], coords_set: Set[Tuple[int, int]], type: str
    ) -> bool:
        if type == "vertical":
            return any(
                [(coord_tup[0] + off, coord_tup[1]) in coords_set for off in [-1, 1]]
            )
        elif type == "horizontal":
            return any(
                [(coord_tup[0], coord_tup[1] + off) in coords_set for off in [-1, 1]]
            )
        else:
            raise ValueError("Invalid type")

    already_assigned_coords = set()
    lines = list()
    for coords in adj_set:
        if coords in already_assigned_coords:
            continue

        # check vertical line
        line = deque([coords])
        while (line[0][0] - 1, line[0][1]) in adj_set and _are_sides_in_coords(
            (line[0][0] - 1, line[0][1]), coords_set, "horizontal"
        ):
            line.appendleft((line[0][0] - 1, line[0][1]))
        while (line[-1][0] + 1, line[-1][1]) in adj_set and _are_sides_in_coords(
            (line[-1][0] + 1, line[-1][1]), coords_set, "horizontal"
        ):
            line.append((line[-1][0] + 1, line[-1][1]))
        if len(line) > 1:
            already_assigned_coords.update(line)
            lines.append(line)
            continue

        # check vertical line
        while (line[0][0], line[0][1] - 1) in adj_set and _are_sides_in_coords(
            (line[0][0], line[0][1] - 1), coords_set, "vertical"
        ):
            line.appendleft((line[0][0], line[0][1] - 1))
        while (line[-1][0], line[-1][1] + 1) in adj_set and _are_sides_in_coords(
            (line[-1][0], line[-1][1] + 1), coords_set, "vertical"
        ):
            line.append((line[-1][0], line[-1][1] + 1))
        if len(line) > 1:
            already_assigned_coords.update(line)
            lines.append(line)
    return lines


def solve_level2(filename: str):
    lines = read_input_lines(filename)
    array = get_array(lines)
    coords_to_region = assign_regions_to_array(array)
    region_to_coords = inverse_coords_to_region(coords_to_region)
    price = 0
    for coords in region_to_coords.values():
        adjacent_counter = {
            xy: count
            for xy, count in get_adjacent_positions_counter(coords).items()
            if xy not in coords
        }
        lines = group_coords_by_straight_lines(adjacent_counter.keys(), coords)
        assigned_in_lines_counter = Counter(chain.from_iterable(lines))
        extra_unitary_fences = sum(
            max(adjacent_counter[coord] - assigned_in_lines_counter[coord], 0)
            for coord in adjacent_counter
        )
        print(
            get_region_area(coords),
            (len(lines)),
            (extra_unitary_fences),
            get_region_area(coords) * (len(lines) + extra_unitary_fences),
        )
        price += get_region_area(coords) * (len(lines) + extra_unitary_fences)

    return price


if __name__ == "__main__":

    current_directory = os.path.dirname(__file__)

    sample_file = f"{current_directory}/sample1.txt"
    sample_file2 = f"{current_directory}/sample2.txt"
    filename1 = f"{current_directory}/input1.txt"
    filename2 = f"{current_directory}/input2.txt"

    # get_input_if_not_exists(2024, current_directory, 1)
    # print(solve_level1(filename1))
    get_input_if_not_exists(2024, current_directory, 2)
    print(solve_level2(filename1))
