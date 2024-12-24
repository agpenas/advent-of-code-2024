import os
from code_logic import solve_level1, solve_level2

current_directory = os.path.dirname(__file__)


class TestAdventOfCode:

    def test_part1_sample(self):
        assert solve_level1(f"{current_directory}/sample1.txt") == 2024

    def test_part1_input(self):
        assert solve_level1(f"{current_directory}/input1.txt") == 42883464055378

    def test_part2_input(self):
        assert (
            solve_level2(f"{current_directory}/input2.txt")
            == "dqr,dtk,pfw,shh,vgs,z21,z33,z39"
        )
