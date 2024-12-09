import os
from code_logic import solve_level1, solve_level2

current_directory = os.path.dirname(__file__)


class TestAdventOfCode:

    def test_part1_sample(self):
        assert solve_level1(f"{current_directory}/sample1.txt") == 1928

    def test_part1_input(self):
        assert solve_level1(f"{current_directory}/input1.txt") == 6421128769094

    def test_part2_sample(self):
        assert solve_level2(f"{current_directory}/sample1.txt") == 2858

    def test_part2_input(self):
        assert solve_level2(f"{current_directory}/input2.txt") == 6448168620520
