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


def defrag(udm: List[str]) -> List[str]:

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


def checksum(ddm: List[str]) -> int:
    the_checksum = 0
    for i, c in enumerate(ddm):
        if c == free_space_char:
            break
        the_checksum += i * int(c)

    return the_checksum


def part1(input: str) -> int:
    udm = uncompress_disk_map(input)
    ddm = defrag(udm)
    return checksum(ddm)
    

if __name__ == '__main__':
    ### THE TESTS
    example_input = '''12345'''

    udm = uncompress_disk_map(example_input)
    print(udm)
    print(defrag(udm))

    example_input = '''2333133121414131402'''

    udm = uncompress_disk_map(example_input)
    print(udm)
    print(defrag(udm))

    ex_result = part1(example_input)
    assert ex_result == 1928, f'Expected 1928, got {ex_result}'

    ### THE REAL THING
    puzzle_input = helper.read_input()
    print(f'Part 1: {part1(puzzle_input)}')
    print(f'Part 2: {""}')
