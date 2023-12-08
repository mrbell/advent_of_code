from __future__ import annotations
from typing import List, Tuple, Dict
from dataclasses import dataclass
from math import lcm
import helper


@dataclass
class Node:
    name: str
    left: str
    right: str

    def __post_init__(self):
        self.is_start = self.name[-1] == 'A'
        self.is_end = self.name[-1] == 'Z'
        self.is_dead_end = self.left == self.name and self.right == self.name

    def step(self, direction: str, nodes: Dict[str, Node]) -> Node:
        if direction == 'L':
            return nodes[self.left]
        elif direction == 'R':
            return nodes[self.right]
        else:
            raise ValueError(f'Unknown direction {direction}')

    def __repr__(self) -> str:
        return f'Node({self.name}, {self.left}, {self.right})'


def parse_nodes(node_input: List[str]) -> Dict[str, Node]:
    nodes = {}
    for line in node_input:
        name, children = line.split(' = ')
        children = children[1:-1].split(', ')

        nodes[name] = Node(name, children[0], children[1])
    return nodes


def parse_input(puzzle_input: str) -> Tuple[str, Dict[str, Node]]:
    puzzle_input = puzzle_input.strip().split('\n\n')
    turns = puzzle_input[0]
    nodes = parse_nodes(puzzle_input[1].split('\n'))
    return turns, nodes


def part1(puzzle_input: str) -> int:
    turns, nodes = parse_input(puzzle_input)
    current_node = nodes['AAA']
    turn_ndx = 0
    steps = 0
    while current_node.name != 'ZZZ':
        current_node = current_node.step(turns[turn_ndx], nodes)
        turn_ndx = (turn_ndx + 1) % len(turns)
        steps += 1
    return steps


def part2(puzzle_input: str) -> int:
    turns, nodes = parse_input(puzzle_input)
    current_nodes = [nodes[node] for node in nodes if nodes[node].is_start]
    turn_ndx = 0
    steps = 0
    path_ends = [{} for _ in current_nodes]
    while not all(node.is_end for node in current_nodes):
        current_nodes = [node.step(turns[turn_ndx], nodes) for node in current_nodes]
        if any(node.is_dead_end for node in current_nodes):
            raise ValueError('Dead end')
        turn_ndx = (turn_ndx + 1) % len(turns)
        steps += 1
        
        for i, node in enumerate(current_nodes):
            if node.is_end:
                if  node.name not in path_ends[i]:
                    path_ends[i][node.name] = [steps]
                else:
                    path_ends[i][node.name].append(steps)
                if all(len(pe) >= 1 for pe in path_ends):
                    vals = [list(pe.values())[0][0] for pe in path_ends]
                    return lcm(*vals)


if __name__ == '__main__':
    ### THE TESTS
    test_input = '''RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)'''

    assert part1(test_input) == 2

    test_input2 = '''LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)'''
    assert part1(test_input2) == 6
    
    test_input3 = '''LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)'''
    assert part2(test_input3) == 6


    ### THE REAL THING
    puzzle_input = helper.read_input()
    print(f'Part 1: {part1(puzzle_input)}')
    print(f'Part 2: {part2(puzzle_input)}')
