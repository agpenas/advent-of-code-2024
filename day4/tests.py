from code_logic import solve_level1, solve_level2


class TestAdventOfCode:

    def test_part1_sample(self):
        assert solve_level1("day4/sample1.txt") == 18

    def test_part1_input(self):
        assert solve_level1("day4/input2.txt") == 2464

    def test_part2_sample(self):
        assert solve_level2("day4/sample1.txt") == 9

    def test_part2_input(self):
        assert solve_level2("day4/input2.txt") == 1982
