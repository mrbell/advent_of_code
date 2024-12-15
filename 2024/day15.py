from typing import List, Tuple, Optional
import helper


WarehouseMap = List[List[str]]


def parse_input(input: str) -> Tuple[WarehouseMap, str]:
    the_map, moves = input.split('\n\n')
    the_map = the_map.split('\n')
    return [[c for c in row] for row in the_map], moves.replace('\n', '')


def scale_up_map(the_map: WarehouseMap) -> WarehouseMap:
    new_map = []
    for row in the_map:
        new_row = []
        for col in row:
            match col:
                case '@':
                    new_row.extend(['@', '.'])
                case 'O':
                    new_row.extend(['[', ']'])
                case '.':
                    new_row.extend(['.', '.'])
                case '#':
                    new_row.extend(['#', '#'])
                case _:
                    raise ValueError(f'Invalid character: {col}')
        new_map.append(new_row)
    return new_map


def find_robot(the_map: WarehouseMap) -> Tuple[int, int]:
    for y, row in enumerate(the_map):
        for x, cell in enumerate(row):
            if cell == '@':
                return x, y


def make_moves(the_map: WarehouseMap, moves: str, map_type: str='small', verbose: bool=False) -> WarehouseMap:
    if map_type == 'small':
        move_fn = make_move
    else:
        move_fn = make_move_larger_map

    if verbose:
        print_map(the_map)

    position = find_robot(the_map)
    for move in moves:
        the_map, position = move_fn(the_map, position, move)
        if verbose:
            print()
            print(f'Move: {move}')
            print_map(the_map)
    return the_map


def make_move(the_map: WarehouseMap, position: Tuple[int, int], move: str) -> Tuple[WarehouseMap, Tuple[int, int]]:   
    x, y = position
    if move == '^':
        new_position = (x, y - 1)
    elif move == 'v':
        new_position = (x, y + 1)
    elif move == '<':
        new_position = (x - 1, y)
    elif move == '>':
        new_position = (x + 1, y)
    else:
        raise ValueError(f'Invalid move: {move}')
    new_x, new_y = new_position

    if the_map[new_y][new_x] == '#':
        return the_map, position
    elif the_map[new_y][new_x] == '.':
        my_char = the_map[y][x]
        the_map[y][x] = '.'
        the_map[new_y][new_x] = my_char
        return the_map, new_position
    else:
        the_map, neighbor_position = make_move(the_map, new_position, move)
        if neighbor_position == new_position:
            return the_map, position
        else:
            the_map, position = make_move(the_map, position, move)
            return the_map, position


def move_obj(the_map: WarehouseMap, position: Tuple[int, int], new_position: Tuple[int, int]) -> WarehouseMap:
    if the_map[position[1]][position[0]] == '@':
        my_char = ['@']
        new_positions = [new_position]
        positions = [position]
    elif the_map[position[1]][position[0]] == '[':
        my_char = ['[', ']']
        positions = [position, (position[0] + 1, position[1])]
        new_positions = [new_position, (new_position[0] + 1, new_position[1])]
    elif the_map[position[1]][position[0]] == ']':
        my_char = ['[', ']']
        positions = [(position[0] - 1, position[1]), position]
        new_positions = [(new_position[0] - 1, new_position[1]), new_position]
    else:
        raise ValueError(f'Invalid character: {the_map[position[1]][position[0]]}')
    
    for char, new_position in zip(my_char, new_positions):
        if the_map[new_position[1]][new_position[0]] != '.':
            raise ValueError(f'Invalid move: {new_position}')
        the_map[new_position[1]][new_position[0]] = char
    for position in positions:
        the_map[position[1]][position[0]] = '.'
    return the_map


def make_move_larger_map(the_map: WarehouseMap, position: Tuple[int, int], move: str) -> Tuple[WarehouseMap, Tuple[int, int]]:

    if move in ['<', '>']:
        # Moving left and right is easy, same as with the smaller map
        the_map, position = make_move(the_map, position, move)
        return the_map, position

    else:
        x, y = position
        if move == '^':
            new_position = (x, y - 1)
        elif move == 'v':
            new_position = (x, y + 1)
        else:    
            raise ValueError(f'Invalid move: {move}')
        
        my_char = the_map[y][x]
        if my_char == '@':
            my_char = ['@']
            new_positions = [new_position]
        elif my_char == '[':
            my_char = ['[', ']']
            new_positions = [new_position, (new_position[0] + 1, new_position[1])]
        elif my_char == ']':
            my_char = ['[', ']']
            position = (x - 1, y)
            new_positions = [(new_position[0] - 1, new_position[1]), new_position]
        else:
            raise ValueError(f'Invalid character: {my_char}')
        neighbor_chars = [the_map[y][x] for x, y in new_positions]

        if any(c == '#' for c in neighbor_chars):
            # There is a wall in the way, can't move
            return the_map, position
        elif all(c == '.' for c in neighbor_chars):
            # There is nothing in the way, just move
            the_map = move_obj(the_map, position, new_position)
            return the_map, new_position
        elif neighbor_chars == [']', '[']:
            # A box needs to push two other boxes
            other_boxes = [  # left sides of the two other boxes
                (new_positions[0][0] - 1, new_positions[0][1]),
                (new_positions[1][0], new_positions[1][1])
            ]
            if all(check_move(the_map, other_box, move) for other_box in other_boxes):
                for other_box in other_boxes:
                    the_map, new_position = make_move_larger_map(the_map, other_box, move)
                the_map = move_obj(the_map, position, new_positions[0])
                return the_map, new_positions[0]
            else:
                return the_map, position
        else:
            # The robot is moving with a box in front of it
            # or a box needs to push one other box

            # Find left side of the neighboring box
            if neighbor_chars[0] == '[':
                neighbor_position = new_positions[0]
            elif neighbor_chars[0] == ']':
                neighbor_position = (new_positions[0][0] - 1, new_positions[0][1])
            else:
                neighbor_position = new_positions[1]
            
            the_map, new_neighbor_position = make_move_larger_map(the_map, neighbor_position, move)
            if new_neighbor_position == neighbor_position:
                return the_map, position
            else:
                the_map, position = make_move_larger_map(the_map, position, move)
                return the_map, position


def check_move(the_map: WarehouseMap, position: Tuple[int, int], move: str) -> bool:
    x, y = position
    if move == '^':
        new_positions = [
            (x, y - 1),
            (x + 1, y - 1)
        ]
    elif move == 'v':
        new_positions = [
            (x, y + 1),
            (x + 1, y + 1)
        ]
    else:
        raise ValueError(f'Invalid move: {move}')
    new_chars = [the_map[new_y][new_x] for new_x, new_y in new_positions]

    if '#' in new_chars:
        # Wall in the way, can't move
        return False
    elif all(c == '.' for c in new_chars):
        # Nothing in the way, can move
        return True
    elif new_chars == ['[', ']']:
        # One box needs to push one other box directly in line
        return check_move(the_map, new_positions[0], move)
    elif new_chars == ['.', '[']:
        # One box needs to push one other box, offset to the right
        return check_move(the_map, new_positions[1], move)
    elif new_chars == [']', '.']:
        # One box needs to push one other box, offset to the left
        return check_move(the_map, (new_positions[0][0]-1, new_positions[0][1]), move)
    else:
        # One box needs to push two other boxes
        return check_move(the_map, (new_positions[0][0]-1, new_positions[0][1]), move) and check_move(the_map, new_positions[1], move)
        

def gps_coordinates(the_map: WarehouseMap) -> int:
    
    gps = 0
    for i, row in enumerate(the_map):
        for j, cell in enumerate(row):
            if cell == 'O' or cell == '[':
                gps += i * 100 + j
    return gps


def part1(input: str) -> int:
    the_map, moves = parse_input(input)
    the_map = make_moves(the_map, moves)
    return gps_coordinates(the_map)


def part2(input: str) -> int:
    the_map, moves = parse_input(input)
    the_map = scale_up_map(the_map)
    the_map = make_moves(the_map, moves, 'large')
    return gps_coordinates(the_map)


def print_map(the_map: WarehouseMap):
    for row in the_map:
        print(''.join(row))


if __name__ == '__main__':
    ### THE TESTS
    example_input = '''########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<'''
    result = part1(example_input)
    helper.check(result, 2028)

    example_input = '''#######
#...#.#
#.....#
#..OO@#
#..O..#
#.....#
#######

<vv<<^^<<^^'''
    result = part2(example_input)

    example_input = '''##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^'''

    result = part1(example_input)
    helper.check(result, 10092)
    
    result = part2(example_input)
    helper.check(result, 9021)

    ### THE REAL THING
    puzzle_input = helper.read_input()
    print(f'Part 1: {part1(puzzle_input)}')
    print(f'Part 2: {part2(puzzle_input)}')
