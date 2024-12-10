from typing import List, Tuple
import helper


free_space_char = '.'


def uncompress_disk_map(disk_map: str) -> List[str]:
    
    uncompressed_disk_map = []
    file_id = 0

    for i, c in enumerate(disk_map):

        val = int(c)

        if i % 2 == 1:
            uncompressed_disk_map += [free_space_char] * val
        else:
            uncompressed_disk_map += [str(file_id)] * val
            file_id += 1 

    return uncompressed_disk_map


def fragment_disk(udm: List[str]) -> List[str]:

    ddm = []
    
    current_block_address = len(udm) - 1

    for i in range(len(udm)):
        if (i >= current_block_address and udm[i] == free_space_char) or (i > current_block_address):
            break

        if udm[i] == free_space_char:
            for j in range(current_block_address, i, -1):
                if udm[j] != free_space_char:
                    break
            ddm.append(udm[j])
            current_block_address = j - 1
        else:
            ddm.append(udm[i])

    ddm = ddm + [free_space_char] * (len(udm) - len(ddm))

    return ddm


def get_bounds(dm: List[str], c: str, start: int=0) -> Tuple[int, int]:
    
    try:
        start_ndx = dm.index(c, start)
    except ValueError:
        return (None, None)

    end_ndx = start_ndx + 1

    while end_ndx < len(dm) and dm[end_ndx] == c:
        end_ndx += 1

    return (start_ndx, end_ndx)


def compact_disk(udm: List[str], verbose: bool=False) -> List[str]:
    file_to_move = max(int(val) for val in udm if val != free_space_char)
    
    ddm = [str(val) for val in udm]

    while file_to_move > 0:
        if verbose:
            print(f'File to move: {file_to_move}')

        file_pos_start, file_pos_end = get_bounds(udm, str(file_to_move))

        free_space_start, free_space_end = 0, 0

        while True:
            free_space_start, free_space_end = get_bounds(ddm[:file_pos_start], free_space_char, free_space_end)

            if free_space_start is None:
                # No more free space
                break
            elif free_space_end - free_space_start >= file_pos_end - file_pos_start:
                # Found enough free space
                ddm = (
                    ddm[:free_space_start] + 
                    [str(file_to_move)] * (file_pos_end - file_pos_start) + 
                    ddm[free_space_start + (file_pos_end - file_pos_start):]
                )
                ddm = (
                    ddm[:file_pos_start] + 
                    [free_space_char] * (file_pos_end - file_pos_start) + 
                    ddm[file_pos_end:]
                )
                break

        file_to_move -= 1

    return ddm


def checksum(ddm: List[str]) -> int:
    the_checksum = 0
    for i, c in enumerate(ddm):
        if c == free_space_char:
            continue
        the_checksum += i * int(c)

    return the_checksum


def part1(input: str) -> int:
    udm = uncompress_disk_map(input)
    ddm = fragment_disk(udm)
    return checksum(ddm)


def part2(input: str, verbose: bool=False) -> int:
    udm = uncompress_disk_map(input)
    if verbose:
        print(''.join(udm))
    ddm = compact_disk(udm, verbose)
    if verbose:
        print(''.join(ddm))
    return checksum(ddm)
    

if __name__ == '__main__':
    ### THE TESTS
    example_input = '''12345'''
    ex_result = part2(example_input)

    example_input = '''2333133121414131402'''
    ex_result = part1(example_input)
    assert ex_result == 1928, f'Expected 1928, got {ex_result}'
    ex_result = part2(example_input, True)
    assert ex_result == 2858, f'Expected 2858, got {ex_result}'

    ### THE REAL THING
    puzzle_input = helper.read_input()
    print(f'Part 1: {part1(puzzle_input)}')
    print(f'Part 2: {part2(puzzle_input, True)}')
