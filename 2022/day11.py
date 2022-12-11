from typing import List, Tuple, Dict
import math
from collections import defaultdict
import helper


class Item(object):
    def __init__(self, value: int):
        self.max_factor = 1
        self.prime_factors = self._prime_factors(value)

    def _prime_factors(self, value: int) -> Dict[int, int]:
        factors = defaultdict(lambda: 0)
        while value % 2 == 0:
            self.max_factor = 2
            factors[2] += 1
            value //= 2
        
        for d in [3, 5, 7, 11, 13, 17, 19, 23]:  # range(3, int(math.sqrt(value)) + 1, 2):
            while value % d == 0:
                self.max_factor = d
                factors[d] += 1
                value //= d
            
        if value > 2:
            if value > self.max_factor:
                self.max_factor = value
            factors[value] += 1
        return factors
    
    @property
    def value(self) -> int:
        val = 1
        for k in self.prime_factors:
            val *= k ** self.prime_factors[k]
        return val
    
    def __mul__(self, other: 'Item') -> 'Item':
        new_item = Item(1)
        for k in self.prime_factors:
            new_item.prime_factors[k] += self.prime_factors[k]
        for k in other.prime_factors:
            new_item.prime_factors[k] += other.prime_factors[k]
        return new_item

    def __truediv__(self, other: 'Item') -> 'Item':
        new_item = Item(1)
        for k in self.prime_factors:
            new_item.prime_factors[k] += self.prime_factors[k]
        for k in other.prime_factors:
            new_item.prime_factors[k] -= other.prime_factors[k]
        return new_item
    
    def __pow__(self, other: int) -> 'Item':
        new_item = Item(1)
        for k in self.prime_factors:
            new_item.prime_factors[k] += self.prime_factors[k] * other
        return new_item

    def gcd(self, other: 'Item') -> 'Item':
        new_item = Item(1)
        for k in self.prime_factors:
            if k in other.prime_factors:
                new_item.prime_factors[k] = min(self.prime_factors[k], other.prime_factors[k])
        return new_item

    def __add__(self, other: 'Item') -> 'Item':

        gcd = self.gcd(other)
        
        this = self / gcd
        that = other / gcd

        new_item = Item(this.value + that.value)

        return new_item * gcd
    
    def is_factor(self, divisor: int) -> bool:
        if self.prime_factors[divisor] > 0:
            return True
        return False


class Monkey(object):
    def __init__(self, input: List[str]):
        input = [line.strip() for line in input]

        self.id = int(input[0].replace('Monkey ', '').replace(':', ''))
        
        self.items = [
            Item(int(item)) for item in input[1].replace('Starting items: ', '').split(', ')
        ]
        
        in1, op, in2 = input[2].replace('Operation: new = ', '').split(' ')
        assert in1 == 'old'
        
        if in2 == 'old':
            self.operation = lambda x: x ** 2
        elif op == '+':
            self.operation = lambda x: x + Item(int(in2))
        elif op == '*':
            self.operation = lambda x: x * Item(int(in2)) 
        else:
            raise ValueError(f'Unknown operation: {op}')
        
        self.test_val = int(input[3].replace('Test: divisible by ', ''))

        self.true_recipient = int(input[4].replace('If true: throw to monkey ', ''))
        self.false_recipient = int(input[5].replace('If false: throw to monkey ', ''))
        
        self.items_inspected = 0

    def receive_item(self, item: 'Item'):
        self.items.append(item)

    def take_turn(self, worry_reduction: int=3) -> List[Tuple['Item', int]]:
        passed_items = []
        for item in self.items:
            self.items_inspected += 1

            if worry_reduction > 1:
                new_item = Item(self.operation(item).value // worry_reduction)
            elif worry_reduction == 1:
                new_item = self.operation(item)
            else:
                raise ValueError(f'Worry reduction must be an integer greater than or equal to 1, not {worry_reduction}')
            
            if new_item.is_factor(self.test_val):
                passed_items.append((new_item, self.true_recipient))
            else:
                passed_items.append((new_item, self.false_recipient))
        self.items = []
        return passed_items


def keep_away(monkeys: List[Monkey], n_rounds: int=20, verbose: bool=False, worry_reduction: int=3):
    rounds = 0
    while rounds < n_rounds:
        for monkey in monkeys:
            if len(monkey.items) == 0:
                continue
            passed_items = monkey.take_turn(worry_reduction)
            for item, recipient in passed_items:
                monkeys[recipient].receive_item(item)
        rounds += 1

        if verbose and (rounds == 1 or rounds == 20 or rounds % 40 == 0):
            print(f'== After round {rounds} ==')
            for monkey in monkeys:
                print(f'Monkey {monkey.id} inspected items {monkey.items_inspected} times')
            print()


def monkey_business(monkeys: List[Monkey]) -> int:
    sorted_monkeys = sorted(monkeys, key=lambda monkey: monkey.items_inspected, reverse=True)
    mb = 1
    for monkey in sorted_monkeys[:2]:
        mb *= monkey.items_inspected

    return mb


if __name__ == '__main__':
    ### THE TESTS
    test_input = '''Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1'''.split('\n\n')
    monkeys = [Monkey(input.split('\n')) for input in test_input]
    keep_away(monkeys)
    assert monkey_business(monkeys) == 10605

    # item = Item(1023454)
    # print('\n'.join(f'{k} ** {item.prime_factors[k]}' for k in item.prime_factors))

    monkeys = [Monkey(input.split('\n')) for input in test_input]
    keep_away(monkeys, n_rounds=1000, verbose=True, worry_reduction=1)
    # assert monkey_business(monkeys) == 2713310158

    ### THE REAL THING
    puzzle_input = helper.read_input().split('\n\n')
    monkeys = [Monkey(input.split('\n')) for input in puzzle_input]
    keep_away(monkeys)
    print(f'Part 1: {monkey_business(monkeys)}')
    monkeys = [Monkey(input.split('\n')) for input in puzzle_input]
    keep_away(monkeys, n_rounds=85, worry_reduction=1, verbose=True)
    print(f'Part 2: {monkey_business(monkeys)}')
