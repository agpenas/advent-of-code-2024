import os
from code_logic import solve_level1, solve_level2

current_directory = os.path.dirname(__file__)


class TestAdventOfCode:

    def test_part1_sample(self):
        assert solve_level1(f"{current_directory}/sample1.txt", 11, 7) == 12

    def test_part1_input(self):
        assert solve_level1(f"{current_directory}/input1.txt", 101, 103) == 222901875

    # No tests for part two, just looking at nice pictures from time to time
    # Anyway, answer was 6242 (so 6243 seconds) for this input file
