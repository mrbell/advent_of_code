from typing import List, Union, Tuple, Any
from itertools import zip_longest
import helper


def parse_list(inp_line: str, pos: int=1) -> Tuple[int, List[Any]]:

    to_return = []
    current_val = ''

    while pos < len(inp_line):
        c = inp_line[pos]
        if c == '[':
            pos, item = parse_list(inp_line, pos + 1)
            to_return.append(item)
        elif c == ']':
            if current_val != '':
                to_return.append(int(current_val))
            return pos + 1, to_return
        elif c == ',':
            pos += 1
            if current_val != '':
                to_return.append(int(current_val))
            current_val = '' 
            continue
        else:
            pos += 1
            current_val += c
    
    return pos, to_return


def parse_packet_pairs(inp: str) -> List[Tuple[Union[int, List[Any]]]]:
    
    packet_pairs = []
    
    packet_pairs_def = inp.split('\n\n')

    for packet_pair_def in packet_pairs_def:
        packet_pair = packet_pair_def.split('\n')
        this_pair  = []
        for pp in packet_pair:
            # I know I could just use literal_eval() here, but I wanted to write my own parser
            _, parsed_packet_pair = parse_list(pp)
            this_pair.append(parsed_packet_pair)
        packet_pairs.append(tuple(this_pair))

    return packet_pairs


def compare(left: Union[int, List[Any]], right: Union[int, List[Any]]) -> int:
    if isinstance(left, int) and isinstance(right, int):
        return (right - left) // abs(right - left) if left != right else 0
    elif isinstance(left, int) and isinstance(right, list):
        return compare([left], right)
    elif isinstance(left, list) and isinstance(right, int):
        return compare(left, [right])
    else:  # both are lists
        for lv, rv in zip_longest(left, right, fillvalue=None):
            if rv is None:
                return -1
            elif lv is None:
                return 1
            else:
                cmp = compare(lv, rv)
                if cmp != 0:
                    return cmp
        return 0


def sort_packets(packet_pairs: List[Tuple[List[Union[int, List[Any]]]]]) -> List[Union[int, List[Any]]]:
    compare_results = [compare(*pp) for pp in packet_pairs]
    sorted_pairs = []
    for i, v in enumerate(compare_results):
        if v >= 0:
            sorted_pairs.append(packet_pairs[i])
        else:
            sorted_pairs.append((
                packet_pairs[i][1], packet_pairs[i][0]
            ))
    
    sorted_packets = [
        [[2]], [[6]]
    ]
    
    for i, pp in enumerate(sorted_pairs):
        packet_index = 0
        for packet in pp:
            while packet_index <= len(sorted_packets):
                if packet_index == len(sorted_packets):
                    sorted_packets.append(packet)
                    break
                elif compare(packet, sorted_packets[packet_index]) >= 0:
                    sorted_packets.insert(packet_index, packet)
                    break
                
                packet_index += 1
    
    return sorted_packets


def decoder_key(sorted_packets: List[Union[int, List[Any]]]) -> int:

    dkey = 1
    divider_packets = [
        [[2]], [[6]]
    ]
    dpi = 0
    for i, packet in enumerate(sorted_packets, 1):
        if packet == divider_packets[dpi]:
            dpi += 1
            dkey *= i
        
        if dpi > 1:
            break
    return dkey


if __name__ == '__main__':
    ### THE TESTS
    test_input = '''[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]'''

    test_packet_pairs = parse_packet_pairs(test_input)
    compare_results = [compare(*pp) for pp in test_packet_pairs]
    assert sum(i+1 for i, v in enumerate(compare_results) if v > 0) == 13
    sorted_packets = sort_packets(test_packet_pairs)
    assert decoder_key(sorted_packets) == 140

    ### THE REAL THING
    puzzle_input = helper.read_input()
    packet_pairs = parse_packet_pairs(puzzle_input)
    compare_results = [compare(*pp) for pp in packet_pairs]
    result = sum(i+1 for i, v in enumerate(compare_results) if v > 0)
    print(f'Part 1: {result}')
    sorted_packets = sort_packets(packet_pairs)
    print(f'Part 2: {decoder_key(sorted_packets)}')
