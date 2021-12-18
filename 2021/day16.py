import helper
from day03 import bin2dec


hex_bin_map = {
    '0': '0000',
    '1': '0001',
    '2': '0010',
    '3': '0011',
    '4': '0100',
    '5': '0101',
    '6': '0110',
    '7': '0111',
    '8': '1000',
    '9': '1001',
    'A': '1010',
    'B': '1011',
    'C': '1100',
    'D': '1101',
    'E': '1110',
    'F': '1111'
}


def parse_packet(packet: str):
    packet_version = bin2dec(packet[:3])
    packet_type = bin2dec(packet[3:6])
    pos = 6

    if packet_type == 4:  ## literal
        literal_val = ''
        while True:
            literal_val += packet[pos + 1: pos + 5]
            prefix = packet[pos]
            pos += 5
            if prefix == '0':
                break
        literal_val = bin2dec(literal_val)
        return [{
            'type': packet_type,
            'version': packet_version,
            'contents': [literal_val],
            'sum_of_versions': packet_version
        }], pos
    else:  ## operator
        length_type_id = int(packet[pos])
        if length_type_id == 0:
            subpacket_bit_length = bin2dec(packet[pos + 1:pos + 16])
            pos += 16
            sub_packets = []
            end_of_packet = pos + subpacket_bit_length
            while pos < end_of_packet:
                these_sub_packets, sub_pos = parse_packet(packet[pos:end_of_packet])
                sub_packets.extend(these_sub_packets)
                pos += sub_pos
            pos = end_of_packet
            
        else:
            number_of_subpackets = bin2dec(packet[pos + 1: pos + 12])
            pos += 12
            sub_packets = []
            for _ in range(number_of_subpackets):
                these_sub_packets, sub_pos = parse_packet(packet[pos:])
                pos += sub_pos
                sub_packets.extend(these_sub_packets)
            
        return [{
            'type': packet_type, 
            'version': packet_version,
            'contents': sub_packets, 
            'sum_of_versions': packet_version + sum(sp['sum_of_versions'] for sp in sub_packets)
        }], pos


def convert_hex_to_bin_packet(hex_packet: str) -> str:
    bin_packet = ''
    for c in hex_packet:
        bin_packet += hex_bin_map[c]
    return bin_packet


def evaluate_packets(packet):

    match packet['type']:
        case 4:
            return packet['contents'][0]
        case 0:
            return sum(evaluate_packets(p) for p in packet['contents'])
        case 1:
            prod = 1
            for p in packet['contents']:
                prod *= evaluate_packets(p)
            return prod
        case 2:
            return min(evaluate_packets(p) for p in packet['contents'])
        case 3:
            return max(evaluate_packets(p) for p in packet['contents'])
        case 5:
            
            first_val = evaluate_packets(packet['contents'][0])
            second_val = evaluate_packets(packet['contents'][1])
            return 1 if first_val > second_val else 0
        case 6:
            first_val = evaluate_packets(packet['contents'][0])
            second_val = evaluate_packets(packet['contents'][1])
            return 1 if first_val < second_val else 0
        case 7:
            first_val = evaluate_packets(packet['contents'][0])
            second_val = evaluate_packets(packet['contents'][1])
            return 1 if first_val == second_val else 0


if __name__ == '__main__':
    ### THE TESTS
    test_packet = 'D2FE28'
    test_packet = convert_hex_to_bin_packet(test_packet)
    assert test_packet == '110100101111111000101000'
    packets = parse_packet(test_packet)[0][0]
    assert packets['version'] == 6 and packets['type'] == 4 and packets['contents'][0] == 2021
    test_packet = '38006F45291200'
    test_packet = convert_hex_to_bin_packet(test_packet)
    packets, _ = parse_packet(test_packet)

    test_packet = convert_hex_to_bin_packet('8A004A801A8002F478')
    packets, _ = parse_packet(test_packet)
    assert packets[0]['sum_of_versions'] == 16
    test_packet = convert_hex_to_bin_packet('620080001611562C8802118E34')
    packets, _ = parse_packet(test_packet)
    assert sum(p['sum_of_versions'] for p in packets) == 12
    test_packet = convert_hex_to_bin_packet('C0015000016115A2E0802F182340')
    packets, _ = parse_packet(test_packet)
    assert sum(p['sum_of_versions'] for p in packets) == 23
    test_packet = convert_hex_to_bin_packet('A0016C880162017C3686B18A3D4780')
    packets, _ = parse_packet(test_packet)
    assert sum(p['sum_of_versions'] for p in packets) == 31
    test_packet = convert_hex_to_bin_packet('C200B40A82')
    packets, _ = parse_packet(test_packet)
    result = evaluate_packets(packets[0])
    assert result == 3

    ### THE REAL THING
    puzzle_input = helper.read_input().strip()
    bin_packet = convert_hex_to_bin_packet(puzzle_input)
    packets, _ = parse_packet(bin_packet)
    print(f'Part 1: {sum(p["sum_of_versions"] for p in packets)}')
    packet_eval = evaluate_packets(packets[0])
    print(f'Part 2: {packet_eval}')
