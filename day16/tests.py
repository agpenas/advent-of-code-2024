import os

from code_logic import solve_level1, solve_level2

current_directory = os.path.dirname(__file__)


class TestAdventOfCode:

    def test_part1_sample(self):
        assert solve_level1(f"{current_directory}/sample1.txt") == 7036

    def test_part1_sample2(self):
        assert solve_level1(f"{current_directory}/sample2.txt") == 11048

    def test_part1_input(self):
        assert solve_level1(f"{current_directory}/input1.txt") == 135512

    def test_part2_sample(self):
        assert solve_level2(f"{current_directory}/sample1.txt") == 45

    def test_part2_sample2(self):
        assert solve_level2(f"{current_directory}/sample2.txt") == 64

    def test_part2_input(self):
        assert solve_level2(f"{current_directory}/input2.txt") == 541
