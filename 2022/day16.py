from typing import List, Union, Dict, Optional, Set 
import helper


TunnelList = List[str]
Valve = Dict[str, Union[int, TunnelList]]
ValveNetwork = Dict[str, Valve]


def parse_valve_network(network_desc: List[str]) -> ValveNetwork:
    network = {}
    for line in network_desc:
        valve_label = line.replace('Valve ', '').split()[0]
        flow_rate = int(line.split(';')[0].split('=')[1])
        tunnels = line.replace(' valve ', ' valves ').split(' valves ')[1].split(', ')
        network[valve_label] = {
            'flow': flow_rate,
            'tunnels': tunnels
        }
    return network


def shortest_path_len(network: ValveNetwork, start: str, end: str) -> int:
    pass


def find_max_pressure(
    network: ValveNetwork, 
    current_valve: str='AA', 
    t: int=1, 
    pressure_rate: int=0,
    total_pressure: int=0, 
    open_valves: Optional[Set[str]]=None
) -> int:
    
    if not open_valves:
        open_valves = set()
    else:
        open_valves = set(open_valves)

    all_valves = set(network.keys())

    if all_valves == open_valves:
        # All valves are open, we're done, just run out the clock
        return total_pressure + pressure_rate * (30 - t)
    
    closed_valves = all_valves.difference(open_valves)

    if current_valve in open_valves or network[current_valve]['flow'] == 0:
        # Valve is open, move along to another one
        t += 1
    else:
        # We need to open the valve before moving along, and that takes and extra minute
        t += 2
        open_valves.add(current_valve)
        total_pressure += pressure_rate
        pressure_rate += network[current_valve]['flow']
    
    if t > 30:
        return total_pressure

    total_pressure += pressure_rate
    
    if t >= 30:
        return total_pressure

    # TODO: Move along... test moving to each connected valve, tally up pressures, return max
    max_pressure = -1
    for connection in network[current_valve]['tunnels']:
        this_pressure = find_max_pressure(
            network,
            connection,
            t,
            pressure_rate,
            total_pressure,
            open_valves
        )
        if this_pressure > max_pressure:
            max_pressure = this_pressure
    
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

    test_network = parse_valve_network(test_input)
    max_pressure = find_max_pressure(test_network)
    assert max_pressure == 1651

    ### THE REAL THING
    puzzle_input = helper.read_input()
    print(f'Part 1: {""}')
    print(f'Part 2: {""}')
