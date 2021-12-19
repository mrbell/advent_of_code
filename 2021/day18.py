from __future__ import annotations
from math import ceil, floor
from typing import Optional, List
import helper


EXPLODE=0
SPLIT=1
REDUCED=1
UNREDUCED=0
other_place = {'x': 'y', 'y': 'x'}


class SnailNumPair:

    def __init__(
        self, 
        l: int|str|SnailNumPair, 
        r: Optional[int|str|SnailNumPair]=None
    ):
        self._x: int|SnailNumPair
        self._y: int|SnailNumPair
        self.parent: Optional[SnailNumPair] = None
        if isinstance(l, str):
            level = 0
            top_level_comma_position = -1
            for i, char in enumerate(l):
                if char == '[':
                    level += 1
                elif char == ']':
                    level -= 1
                elif char == ',' and level == 1:
                    top_level_comma_position = i
                    break
            x = l[1:top_level_comma_position]
            y = l[top_level_comma_position + 1:-1]

            self.x = SnailNumPair(x) if '[' in x else int(x)
            self.y = SnailNumPair(y) if '[' in y else int(y) 
        else:
            self.x = l
            self.y = r
            self.parent = None
    
    def get_position(self):
        if self.parent is not None:
            return 'x' if self.parent.x == self else 'y'
        return None

    @property
    def x(self) -> int|SnailNumPair:
        return self._x
    
    @x.setter
    def x(self, value: int|SnailNumPair):
        self._x = value
        if isinstance(self._x, SnailNumPair):
            self._x.parent = self

    @property
    def y(self) -> int|SnailNumPair:
        return self._y
    
    @y.setter
    def y(self, value: int|SnailNumPair):
        self._y = value
        if isinstance(self._y, SnailNumPair):
            self._y.parent = self

    def __add__(self, other: SnailNumPair|int) -> SnailNumPair:
        return SnailNumPair(self, other)

    def __repr__(self) -> str:
        return f"SnailNumPair('{str(self)}')"

    def __str__(self) -> str:
        return f'[{str(self.x)},{str(self.y)}]'

    def mag(self) -> int:
        x_mag = 3 * (self.x if isinstance(self.x, int) else self.x.mag())
        y_mag = 2 * (self.y if isinstance(self.y, int) else self.y.mag())
        return x_mag + y_mag

    def explode_add(self, from_place: str, direction: str, value: int, from_within: bool=True) -> int:
        if from_place == direction and self.parent is not None:
            return self.parent.explode_add(self.get_position(), direction, value)
        elif from_place == direction and self.parent is None:
            return 0
        elif from_place != direction and not from_within and isinstance(getattr(self, from_place), int): 
            setattr(
                self, 
                from_place, 
                getattr(self, from_place) + value
            )
            return 1
        elif from_place != direction and from_within and isinstance(getattr(self, other_place[from_place]), int): 
            setattr(
                self, 
                other_place[from_place], 
                getattr(self, other_place[from_place]) + value
            )
            return 1
        else:
            child = getattr(self, other_place[from_place]) if from_within else getattr(self, from_place)
            return child.explode_add(
                from_place, 
                direction,
                value,
                False
            )
    
    def reduce_step(self, level: int=0, passed_action: Optional[int]=None) -> int:

        actions = [passed_action] if passed_action is not None else [EXPLODE, SPLIT]
        
        reduced = UNREDUCED

        for action in actions:
            for place in ['x', 'y']:
                val = getattr(self, place)
                if action == EXPLODE and level == 3 and isinstance(val, SnailNumPair):
                    # next level needs to be exploded
                    child_x, child_y = val.x, val.y
                    setattr(self, place, 0)
                    self.explode_add(place, 'x', child_x)
                    self.explode_add(place, 'y', child_y)
                    reduced = REDUCED
                elif action == SPLIT and isinstance(val, int) and val >= 10: 
                    # value needs to be split
                    reduced = REDUCED
                    new_x = floor(val / 2)
                    new_y = ceil(val / 2)
                    setattr(self, place, SnailNumPair(new_x, new_y))
                elif isinstance(val, SnailNumPair):
                    # reduce the value
                    reduced = val.reduce_step(level+1, action)
                if reduced:
                    return reduced

        return reduced

    def reduce(self):
        while self.reduce_step():
            pass


def sum_snail_numbers(snail_numbers: List[str]) -> SnailNumPair:
    snail_number = SnailNumPair(snail_numbers[0])
    for sn in snail_numbers[1:]:
        snail_number = snail_number + SnailNumPair(sn)
        snail_number.reduce()
    return snail_number


def find_largest_pairwise_sum(snail_numbers: List[str]) -> int:

    magnitudes = []

    for i, sn in enumerate(snail_numbers):
        snail_num_a = SnailNumPair(sn)
        other_snail_numbers = snail_numbers[:i] + snail_numbers[i+1:]
        for osn in other_snail_numbers:
            snail_num_b = SnailNumPair(osn)
            s = snail_num_a + snail_num_b
            s.reduce()
            magnitudes.append(
                s.mag()
            )

    return max(magnitudes)


if __name__ == '__main__':
    ### THE TESTS
    a = SnailNumPair(1,1)
    b = SnailNumPair('[2,2]')
    c = SnailNumPair(3,3)
    d = SnailNumPair(4,4)
    assert str(a+b+c+d) == '[[[[1,1],[2,2]],[3,3]],[4,4]]'

    assert str(SnailNumPair('[[[[1,1],[2,2]],[3,3]],[4,4]]')) == '[[[[1,1],[2,2]],[3,3]],[4,4]]'
    assert SnailNumPair('[[9,1],[1,9]]').mag() == 129

    a = SnailNumPair('[[[[4,3],4],4],[7,[[8,4],9]]]')
    b = SnailNumPair('[1,1]')
    c = a + b
    while c.reduce_step():
        pass
    assert str(c) == '[[[[0,7],4],[[7,8],[6,0]]],[8,1]]' 
    c = a + b
    c.reduce()
    assert str(c) == '[[[[0,7],4],[[7,8],[6,0]]],[8,1]]' 

    a = SnailNumPair('[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]')
    b = SnailNumPair('[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]')
    c = a + b
    c.reduce()
    assert c.mag() == 3993

    example_homework = '''[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]'''.split('\n')

    example_sum = sum_snail_numbers(example_homework)
    assert str(example_sum) == '[[[[6,6],[7,6]],[[7,7],[7,0]]],[[[7,7],[7,7]],[[7,8],[9,9]]]]'
    assert example_sum.mag() == 4140
    assert find_largest_pairwise_sum(example_homework) == 3993

    ### THE REAL THING
    puzzle_input = helper.read_input_lines()
    snail_num_sum = sum_snail_numbers(puzzle_input)
    print(f'Part 1: {snail_num_sum.mag()}')
    print(f'Part 2: {find_largest_pairwise_sum(puzzle_input)}')  # 4770 is too low
