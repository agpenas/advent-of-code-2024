from collections import Counter, defaultdict
import os.path
from typing import List, Tuple
import dotenv

from utils.utils import get_input_if_not_exists, read_input_lines

dotenv.load_dotenv()


## Implementation of PART 1


class LANParty:
    def __init__(self, node_to_neighbors):
        self.node_to_neighbors = node_to_neighbors

    @classmethod
    def from_lines(cls, lines: List[str]):
        node_to_neighbors = defaultdict(list)
        for line in lines:
            node1, node2 = line.split("-")
            node_to_neighbors[node1].append(node2)
            node_to_neighbors[node2].append(node1)
        return cls(node_to_neighbors)

    def get_three_way_games(self):
        three_way_games = set()
        for node, neighbors in self.node_to_neighbors.items():
            for neigh in neighbors:
                third_players = set(neighbors) & set(self.node_to_neighbors[neigh]) - {
                    node,
                    neigh,
                }
                if not third_players:
                    continue
                for third in third_players:
                    sorted_players = tuple(sorted([node, neigh, third]))
                    three_way_games.add(sorted_players)
        return three_way_games

    def add_players_to_game(self, game):
        connection_counter = Counter()
        for player in game:
            connection_counter.update(self.node_to_neighbors[player])
        new_players = [
            player
            for player, count in connection_counter.items()
            if count == len(game) and player not in game
        ]
        if not new_players:
            return
        return [game + tuple([new_player]) for new_player in new_players]


def solve_level1(filename: str):
    lines = read_input_lines(filename)
    lan_party = LANParty.from_lines(lines)

    three_way_games = lan_party.get_three_way_games()
    result = len(
        [game for game in three_way_games if any(node[0] == "t" for node in game)]
    )

    return result


## Implementation of PART 2


def solve_level2(filename: str):
    lines = read_input_lines(filename)
    lan_party = LANParty.from_lines(lines)

    previous_games = lan_party.get_three_way_games()
    while True:
        new_games_list = []
        for game in previous_games:
            new_games = lan_party.add_players_to_game(game)
            if new_games:
                new_games_list.extend(new_games)
        if not new_games_list:
            break
        previous_games = {tuple(sorted(game)) for game in new_games_list}

    return ",".join(sorted(list(previous_games)[0]))


if __name__ == "__main__":

    current_directory = os.path.dirname(__file__)

    sample_file = f"{current_directory}/sample1.txt"
    filename1 = f"{current_directory}/input1.txt"
    filename2 = f"{current_directory}/input2.txt"

    # get_input_if_not_exists(2024, current_directory, 1)
    # print(solve_level1(filename1))
    get_input_if_not_exists(2024, current_directory, 2)
    print(solve_level2(filename2))
