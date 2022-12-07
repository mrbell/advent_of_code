import helper


def find_start_of_packet(buffer: str, window_len=4) -> int:
    for i in range(window_len, len(buffer)):
        win = buffer[(i-window_len):i]
        if len(set(win)) == window_len:
            return i
    return -1


if __name__ == '__main__':
    ### THE TESTS
    tests = [
        ('mjqjpqmgbljsphdztnvjfqwrcgsmlb', 7, 19),
        ('bvwbjplbgvbhsrlpgdmjqwftvncz', 5, 23),
        ('nppdvjthqldpwncqszvftbrmjlhg', 6, 23),
        ('nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg', 10, 29),
        ('zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw', 11, 26)
    ]

    for b, s1, s2 in tests:
        assert find_start_of_packet(b) == s1
        assert find_start_of_packet(b, 14) == s2

    ### THE REAL THING
    puzzle_input = helper.read_input()
    packet_start = find_start_of_packet(puzzle_input)
    print(f'Part 1: {packet_start}')
    packet_start = find_start_of_packet(puzzle_input, 14)
    print(f'Part 2: {packet_start}')
