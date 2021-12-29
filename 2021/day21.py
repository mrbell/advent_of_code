from typing import Dict 
from collections import defaultdict
from itertools import product
from random import randint
import helper


class Die:
    def __init__(self, n_sides=100):
        self.n_sides = n_sides
    def roll(self) -> int:
        return randint(1, self.n_sides)


class DeterministicDie(Die):
    def __init__(self, n_sides=100):
        super().__init__(n_sides)
        self.state = 0
    def roll(self) -> int:
        to_return = self.state % self.n_sides + 1
        self.state += 1
        return to_return


class DiracDiceGame:
    def __init__(self, p1_start: int, p2_start: int, die: Die):
        self.positions = [p1_start, p2_start]
        self.scores = [0, 0]
        self.die = die
        self.current_player = 0
        self.die_rolls = 0

    def take_turn(self):
        position = self.positions[self.current_player]
        score = self.scores[self.current_player]

        roll = sum(self.die.roll() for _ in range(3))

        new_position = ((position - 1) + roll) % 10 + 1
        score += new_position

        self.die_rolls += 3
        self.scores[self.current_player] = score
        self.positions[self.current_player] = new_position

        self.current_player = (self.current_player + 1) % 2

    def winner(self) -> int:
        for i, score in enumerate(self.scores):
            if score >= 1000:
                return i
        return -1


possible_rolls = [sum(vals) for vals in product(range(1,4), range(1,4), range(1,4))]
grouped_rolls = defaultdict(lambda: 0)
for pr in possible_rolls:
    grouped_rolls[pr] += 1


def dirac_game(p1_start: int, p2_start: int, p1_score: int=0, p2_score: int=0, current_player: int=0, turn: int=1) -> Dict[str, int]: 
    results = {'p1_wins': 0, 'p2_wins': 0}
    for i in grouped_rolls:
        n_vals = grouped_rolls[i]
        if current_player == 0:
            p1_pos = (p1_start - 1 + i) % 10 + 1
            new_p1_score = p1_score + p1_pos

            if new_p1_score < 21:
                sub_results = dirac_game(p1_pos, p2_start, new_p1_score, p2_score, 1, turn + 1)
                results['p1_wins'] += n_vals * sub_results['p1_wins']
                results['p2_wins'] += n_vals * sub_results['p2_wins']
            else:
                results['p1_wins'] += n_vals
        else:
            p2_pos = (p2_start - 1 + i) % 10 + 1
            new_p2_score = p2_score + p2_pos

            if new_p2_score < 21:
                sub_results = dirac_game(p1_start, p2_pos, p1_score, new_p2_score, 0, turn + 1)
                results['p1_wins'] += n_vals * sub_results['p1_wins']
                results['p2_wins'] += n_vals * sub_results['p2_wins']
            else:
                results['p2_wins'] += n_vals
    return results


if __name__ == '__main__':
    ### THE TESTS
    test_p1_start = 4
    test_p2_start = 8
    test_game = DiracDiceGame(test_p1_start, test_p2_start, DeterministicDie())
    while test_game.winner() < 0:
        test_game.take_turn()
    assert min(test_game.scores) * test_game.die_rolls == 739785

    test_results = dirac_game(test_p1_start, test_p2_start)
    assert max(test_results.values()) == 444356092776315

    ### THE REAL THING
    puzzle_input = helper.read_input_lines()
    p1_start = int(puzzle_input[0][-1])
    p2_start = int(puzzle_input[1][-1])
    game = DiracDiceGame(p1_start, p2_start, DeterministicDie())
    while game.winner() < 0:
        game.take_turn()
    print(f'Part 1: {min(game.scores) * game.die_rolls}')
    results = dirac_game(p1_start, p2_start)
    print(f'Part 2: {max(results.values())}')
