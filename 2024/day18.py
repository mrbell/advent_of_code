from typing import List, Optional, Tuple
import helper


def get_memory_blocks(input: List[str]) -> List[Tuple[int, int]]:
    return [tuple(map(int, line.split(','))) for line in input]


def make_map(memory_blocks: List[Tuple[int, int]], size: Tuple[int, int], n_bytes: int) -> List[List[str]]:
    memory_map = [['.' for _ in range(size[0])] for _ in range(size[1])]
    for i in range(n_bytes):
        block = memory_blocks[i]
        memory_map[block[1]][block[0]] = '#'
    return memory_map


def print_map(memory_map: List[List[str]]) -> None:
    for row in memory_map:
        print(''.join(row))


def get_neighbors(cell: Tuple[int, int], memory_map: List[List[str]]) -> List[Tuple[int, int]]:
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    neighbors = []
    for direction in directions:
        neighbor = (cell[0] + direction[0], cell[1] + direction[1])
        if 0 <= neighbor[0] < len(memory_map[0]) and 0 <= neighbor[1] < len(memory_map) and memory_map[neighbor[1]][neighbor[0]] != '#':
            neighbors.append(neighbor)
    return neighbors


def dijstra(memory_map: List[List[str]], end: Optional[Tuple[int, int]]=None) -> int:
    start = (0, 0)
    if end is None:
        end = (len(memory_map[0])-1, len(memory_map)-1)
    costs = {}
    queue = []
    for y, row in enumerate(memory_map):
        for x, cell in enumerate(row):
            if cell != '#':
                costs[(x, y)] = float('inf')
                queue.append((x, y))
    costs[start] = 0

    while queue:
        current = min(queue, key=lambda x: costs[x])
        if current == end:
            return costs[current]
        queue.remove(current)
        for neighbor in get_neighbors(current, memory_map):
            new_cost = costs[current] + 1
            if new_cost < costs[neighbor]:
                costs[neighbor] = new_cost
            
    return costs[end]


def part1(puzzle_input: List[str], mem_size: Tuple[int, int], n_bytes: int) -> int:
    memory_blocks = get_memory_blocks(puzzle_input)
    memory_map = make_map(memory_blocks, mem_size, n_bytes)
    return dijstra(memory_map)


def search_for_blockage(memory_blocks: List[Tuple[int, int]], size: Tuple[int, int], non_blockages: List[Tuple[int, int]]) -> int:
    bytes_low = 0
    bytes_high = len(memory_blocks)
    while True:
        n_bytes = (bytes_low + bytes_high) // 2
        memory_map = make_map(memory_blocks, size, n_bytes)
        for non_blockage in non_blockages:
            memory_map[non_blockage[1]][non_blockage[0]] = '.'
        result = dijstra(memory_map)
        if result == float('inf'):
            bytes_high = n_bytes
        else:
            bytes_low = n_bytes
        if bytes_high - bytes_low <= 1:
            return bytes_high


def path_to_blockage(memory_blocks: List[Tuple[int, int]], size: Tuple[int, int], blockage_byte: int, non_blockages: List[Tuple[int, int]]) -> int:
    memory_map = make_map(memory_blocks, size, blockage_byte - 1)
    for non_blockage in non_blockages:
        memory_map[non_blockage[1]][non_blockage[0]] = '.'
    return dijstra(memory_map, memory_blocks[blockage_byte - 1])


def part2(puzzle_input: List[str], mem_size: Tuple[int, int]) -> int:
    memory_blocks = get_memory_blocks(puzzle_input)
    blockage_byte = search_for_blockage(memory_blocks, mem_size, [])
    return ','.join(map(str, memory_blocks[blockage_byte-1]))
    

if __name__ == '__main__':
    ### THE TESTS
    example_input = '''5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0'''.split('\n')
    result = part1(example_input, (7, 7), 12)
    helper.check(result, 22)

    ### THE REAL THING
    puzzle_input = helper.read_input_lines()
    print(f'Part 1: {part1(puzzle_input, (71, 71), 1024)}')
    print(f'Part 2: {part2(puzzle_input, (71, 71))}')

