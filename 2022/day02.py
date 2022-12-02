from typing import List, Tuple
import helper


# X: Y -> X beats Y
matchups = {
    'rock': 'scissors', 
    'paper': 'rock', 
    'scissors': 'paper'
}

inv_matchups = {matchups[k]:k for k in matchups}

opp_key = {
    'A': 'rock',
    'B': 'paper',
    'C': 'scissors'
}

my_key = {
    'X': 'rock',
    'Y': 'paper',
    'Z': 'scissors'
}

shape_scores = {
    'rock': 1,
    'paper': 2,
    'scissors': 3
}


def decrypt_guide_assumed(encrypted_guide):
    guide = []
    for round in encrypted_guide:
        opp_shape, my_shape = round.split()
        guide.append(
            (opp_key[opp_shape], my_key[my_shape])
        )
    return guide


def decrypt_guide(encrypted_guide):
    guide = []
    for round in encrypted_guide:
        opp_shape, desired_outcome = round.split()
        opp_shape = opp_key[opp_shape]

        if desired_outcome == 'X':  # I need to lose
            my_shape = matchups[opp_shape]
        elif desired_outcome == 'Z':  # I need to win
            my_shape = inv_matchups[opp_shape] 
        else:  # I need to draw
            my_shape = opp_shape  
        guide.append((opp_shape, my_shape))
    return guide


def game_score(guide):
    score = 0
    for (opp_shape, my_shape) in guide:
        outcome_score = 0
        if opp_shape == my_shape:
            outcome_score = 3
        elif matchups[my_shape] == opp_shape:
            outcome_score = 6
        shape_score = shape_scores[my_shape]
        score += outcome_score + shape_score
    return score


if __name__ == '__main__':
    ### THE TESTS
    test_guide = '''A Y
B X
C Z
'''.strip('\n').split('\n')

    guide = decrypt_guide_assumed(test_guide)
    assert game_score(guide) == 15
    guide = decrypt_guide(test_guide)
    assert game_score(guide) == 12


    ### THE REAL THING
    puzzle_input = helper.read_input_lines()
    guide = decrypt_guide_assumed(puzzle_input)
    score = game_score(guide)
    print(f'Part 1: {score}')
    guide = decrypt_guide(puzzle_input)
    score = game_score(guide)
    print(f'Part 2: {score}')
