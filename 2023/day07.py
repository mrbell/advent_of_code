from __future__ import annotations
from typing import List, Tuple, Dict
import helper


card_ranks = 'A, K, Q, J, T, 9, 8, 7, 6, 5, 4, 3, 2'.split(', ')
card_ranks_joker_wild = 'A, K, Q, T, 9, 8, 7, 6, 5, 4, 3, 2, J'.split(', ')
hand_types = ['five of a kind', 'four of a kind', 'full house', 'three of a kind', 'two pair', 'one pair', 'high card']


class CamelCardHand(object):
    def __init__(self, the_cards: str, joker_wild: bool = False):
        self.cards = the_cards
        self.joker_wild = joker_wild
        self._hand_type = None
        self._card_rank = card_ranks if not joker_wild else card_ranks_joker_wild

    def __repr__(self):
        return f'CamelCardHand({self.cards})'
    
    def __eq__(self, other: CamelCardHand) -> bool:
        return self.cards == other.cards

    def __lt__(self, other: CamelCardHand) -> bool:
        this_rank = hand_types.index(self.hand_type)
        other_rank = hand_types.index(other.hand_type)
        if this_rank != other_rank:
            return this_rank > other_rank
        else:
            for i, this_card in enumerate(self.cards):
                other_card = other.cards[i]
                if this_card != other_card:
                    return self._card_rank.index(this_card) > self._card_rank.index(other_card)
            return False
    
    def __gt__(self, other: CamelCardHand) -> bool:
        return other < self
    
    def __le__(self, other: CamelCardHand) -> bool:
        return not self > other

    def __ge__(self, other: CamelCardHand) -> bool:
        return not self < other
    
    def __ne__(self, other: CamelCardHand) -> bool:
        return not self == other

    def _calculate_hand_type(self) -> str:

        card_count = self._card_counts()
        
        if len(card_count) == 5:
            return 'high card'
        elif len(card_count) == 1:
            return 'five of a kind'
        elif len(card_count) == 4:
            return 'one pair'
        elif len(card_count) == 3:
            if 3 in card_count.values():
                return 'three of a kind'
            else:
                return 'two pair'
        elif len(card_count) == 2:
            if 2 in card_count.values():
                return 'full house'
            else:
                return 'four of a kind'
        else:
            raise Exception(f'Unexpected card count: {len(card_count)}')
    
    def _card_counts(self) -> Dict[str, int]:
        card_count = {}
        for card in self.cards:
            card_count[card] = card_count.get(card, 0) + 1
        return card_count

    def _calculate_hand_type_joker_wild(self) -> str:
        
        if 'J' not in self.cards:
            return self._calculate_hand_type()
        
        card_count = self._card_counts()
        
        if len(card_count) == 5:
            # The one J can be one of the other 4 cards to make a pair
            return 'one pair'
        elif len(card_count) == 1:
            # All of the cards are J, still a 5oak
            return 'five of a kind'
        elif len(card_count) == 4:
            # If the pair is a J, any other card can 3oak it... if the pair is not a J, the J can 3oak the pair
            return 'three of a kind'
        elif len(card_count) == 3:
            # Two scenarios... XXYYZ or XXXYZ
            # If the 2 pair scenario and Z == J, the best hand is a FH
            # Otherwise the best hand is a 4oak
            if 3 not in card_count.values() and card_count['J'] == 1:
                return 'full house'
            else:
                return 'four of a kind'
        elif len(card_count) == 2:
            # Two scenarios... XXXYY or XXXXY
            # No matter which of them is the J, the best hand is a 5oak
            return 'five of a kind'
        else:
            raise Exception(f'Unexpected card count: {len(card_count)}')

    @property
    def hand_type(self) -> str:
        if self._hand_type is None and not self.joker_wild:
            self._hand_type = self._calculate_hand_type()
        elif self._hand_type is None and self.joker_wild:
            self._hand_type = self._calculate_hand_type_joker_wild()
        return self._hand_type


def parse_hands(puzzle_input: List[str], joker_wild: bool=False) -> List[Tuple[CamelCardHand, int]]:
    hands = []
    for line in puzzle_input:
        cards, score = line.split()
        hands.append((CamelCardHand(cards, joker_wild), int(score)))
    return hands


def part1(puzzle_input: List[str], joker_wild: bool=False) -> int:
    hands = parse_hands(puzzle_input, joker_wild)
    hands = sorted(hands, key=lambda x: x[0])

    return sum([(i + 1) * score for i, (_, score) in enumerate(hands)]) 


def part2(puzzle_input: List[str]) -> int:
    return part1(puzzle_input, joker_wild=True)


if __name__ == '__main__':
    ### THE TESTS
    test_input = '''32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483'''.split('\n')

    test_hand = CamelCardHand('32T3K')
    assert test_hand.hand_type == 'one pair'

    assert part1(test_input) == 6440
    assert part2(test_input) == 5905

    ### THE REAL THING
    puzzle_input = helper.read_input_lines()
    print(f'Part 1: {part1(puzzle_input)}')
    print(f'Part 2: {part2(puzzle_input)}')
