from typing import List, Union, Dict, Optional, Set 
import copy
import helper


TunnelList = List[str]
Valve = Dict[str, Union[int, TunnelList]]
ValveNetwork = Dict[str, Valve]


def cant_open(node: str, network: ValveNetwork) -> bool:
    '''
    Returns True if the node cannot be opened.
    '''
    return network[node]['open']


def through_way_with(node: str, network: ValveNetwork) -> Optional[str]:
    '''
    Returns True if the node is a through-way.
    '''
    for neighbor in network[node]['tunnels']:
        if cant_open(neighbor, network) and (len(network[neighbor]['tunnels']) == 2):
            return neighbor
    return None


def reduce_network(network: ValveNetwork, current_node: Optional[str]=None) -> ValveNetwork:
    
    reduced_network = copy.deepcopy(network) 
    nodes_to_visit = list(network.keys())

    if current_node:
        current_node_open_status = reduced_network[current_node]['open']
        reduced_network[current_node]['open'] = False 

    while nodes_to_visit:
        node = nodes_to_visit.pop()

        if cant_open(node, reduced_network) and (len(reduced_network[node]['tunnels']) == 1):
            # This is a dead end. Remove it.
            neighbor = reduced_network[node]['tunnels'][0]
            reduced_network[neighbor]['tunnels'].remove(node)
            _ = reduced_network.pop(node)
            if neighbor not in nodes_to_visit:
                nodes_to_visit.append(neighbor)
            continue
        elif (
            cant_open(node, reduced_network) and 
            (len(reduced_network[node]['tunnels']) == 2) and 
            (neighbor := through_way_with(node, reduced_network))
        ): 
            try:
                nodes_to_visit.remove(neighbor)
            except ValueError:
                pass

            new_neighbors = list(set(reduced_network[node]['tunnels'].copy() + reduced_network[neighbor]['tunnels'].copy()))
            new_neighbors.remove(node)
            new_neighbors.remove(neighbor)

            new_node = '_'.join(sorted([node, neighbor]))

            reduced_network[new_node] = {
                'flow': reduced_network[node]['flow'] + reduced_network[neighbor]['flow'],
                'open': reduced_network[node]['open'] or reduced_network[neighbor]['open'],
                'move_cost': reduced_network[node]['move_cost'] + reduced_network[neighbor]['move_cost'],
                'tunnels': new_neighbors 
            }

            _ = reduced_network.pop(node)
            _ = reduced_network.pop(neighbor)

            for n in new_neighbors:
                try:
                    reduced_network[n]['tunnels'].remove(node)
                except ValueError:
                    pass
                try:
                    reduced_network[n]['tunnels'].remove(neighbor)
                except ValueError:
                    pass
                reduced_network[n]['tunnels'].append(new_node)
            
            nodes_to_visit.append(new_node)

        else:
            # Can't reduce this node. 
            continue
    
    if current_node:
        reduced_network[current_node]['open'] = current_node_open_status

    return reduced_network


def parse_valve_network(network_desc: List[str]) -> ValveNetwork:
    network = {}
    for line in network_desc:
        valve_label = line.replace('Valve ', '').split()[0]
        flow_rate = int(line.split(';')[0].split('=')[1])
        tunnels = line.replace(' valve ', ' valves ').split(' valves ')[1].split(', ')
        network[valve_label] = {
            'flow': flow_rate,
            'tunnels': tunnels,
            'open': False if flow_rate > 0 else True,
            'move_cost': 1
        }
    return network


def shortest_path_len(network: ValveNetwork, start: str, end: str) -> int:
    '''
    Code up Dijkstra's algorithm.
    '''
    # visited_points = [[False] * len(elev_map.map[0]) for _ in range(len(elev_map.map))]
    visited_points = {n: False for n in network.keys()}

    # least_path_risks = [[1e9] * len(elev_map.map[0]) for _ in range(len(elev_map.map))]
    least_path_times = {n: 1e9 for n in network.keys()}

    current_node = start
    destination_node = end 
    
    least_path_times[current_node] = 0

    while True:
        neighbors = network[current_node]['tunnels']
        neighbors = [
            n for n in neighbors 
            if not visited_points[n]
        ]

        for n in neighbors:
            tentative_dist = network[current_node]['move_cost'] + least_path_times[current_node]
            if tentative_dist < least_path_times[n]:
                least_path_times[n] = tentative_dist
        
        visited_points[current_node] = True

        if visited_points[destination_node]:
            break
        else:
            unvisited_node_risks = []
            for node in visited_points:
                if not visited_points[node]:
                    unvisited_node_risks.append(
                        (node, least_path_times[node])
                    )
            current_node = min(unvisited_node_risks, key=lambda x: x[1])[0]

    return least_path_times[destination_node]


def find_max_pressure(
    network: ValveNetwork, 
    starting_valve: str='AA',
    pressure_rate: int=0,
    pressure: int=0,
    t: int=0
) -> int:

    closed_valves = [v for v in network.keys() if not network[v]['open']]

    if not closed_valves:
        # We've opened all the valves
        max_pressure = pressure + (pressure_rate * (30 - t))
    else:
        reduced_network = reduce_network(network, starting_valve)
        
        max_pressure = pressure
        for test_destination_valve in closed_valves:
            move_cost = shortest_path_len(reduced_network, starting_valve, test_destination_valve)

            dt = move_cost + 1  # Plus 1 to open the valve at the destination
            test_t = t + dt  
            if test_t > 30:
                # We wont have time to get to the valve and open it
                # so just add up the pressure built in the remaining time
                possible_max_pressure = pressure + (pressure_rate * (30 - t))
            else:
                test_pressure = pressure + (pressure_rate * dt) 
                test_pressure_rate = pressure_rate + reduced_network[test_destination_valve]['flow']

                test_network = copy.deepcopy(reduced_network)
                test_network[test_destination_valve]['open'] = True

                possible_max_pressure = find_max_pressure(test_network, test_destination_valve, test_pressure_rate, test_pressure, test_t)

            if possible_max_pressure > max_pressure:
                max_pressure = possible_max_pressure
    
    return max_pressure 


if __name__ == '__main__':
    ### THE TESTS
    test_input = '''Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II'''.split('\n')

    test_network = {
        'AA': {'flow': 20, 'tunnels': ['BB'], 'open': False, 'move_cost': 1},
        'BB': {'flow': 0, 'tunnels': ['CC', 'AA'], 'open': True, 'move_cost': 1},
        'CC': {'flow': 0, 'tunnels': ['DD', 'BB'], 'open': True, 'move_cost': 1},
        'DD': {'flow': 0, 'tunnels': ['CC', 'EE'], 'open': True, 'move_cost': 1},
        'EE': {'flow': 3, 'tunnels': ['FF', 'DD'], 'open': False, 'move_cost': 1},
        'FF': {'flow': 0, 'tunnels': ['EE'], 'open': True, 'move_cost': 1}
    }
    reduced_test_network = reduce_network(test_network)
    assert 'BB_CC_DD' in reduced_test_network
    assert reduced_test_network['BB_CC_DD']['move_cost'] == 3
    assert 'FF' not in reduced_test_network

    reduced_test_network = reduce_network(test_network, 'BB')
    assert 'BB' in reduced_test_network
    assert 'CC_DD' in reduced_test_network
    assert len(reduced_test_network) == 4

    test_network = {
        'AA': {'flow': 10, 'tunnels': ['BB', 'CC'], 'open': False, 'move_cost': 1},
        'BB': {'flow': 0, 'tunnels': ['CC', 'AA'], 'open': True, 'move_cost': 1},
        'CC': {'flow': 0, 'tunnels': ['AA', 'BB'], 'open': True, 'move_cost': 1}
    }
    reduced_test_network = reduce_network(test_network)
    assert 'AA' in reduced_test_network
    assert len(reduced_test_network) == 1

    reduced_test_network = reduce_network(test_network, 'BB')
    assert 'BB' in reduced_test_network
    assert len(reduced_test_network) == 3

    test_network = parse_valve_network(test_input)
    max_pressure = find_max_pressure(test_network)
    assert max_pressure == 1651

    ### THE REAL THING
    puzzle_input = helper.read_input_lines()
    network = parse_valve_network(puzzle_input)
    # network = reduce_network(network, [v for v in network if network[v]['flow'] > 0])
    max_pressure = find_max_pressure(network)
    print(f'Part 1: {max_pressure}')
    print(f'Part 2: {""}')
