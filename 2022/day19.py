from typing import List, Tuple, Optional, Dict
from dataclasses import dataclass 
import helper


@dataclass
class Resources(object):
    ore: int=0
    clay: int=0
    obsidian: int=0
    geode: int=0

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, Resources):
            return NotImplemented
        return all(getattr(self, resource_type) == getattr(__o, resource_type) for resource_type in self.__dict__)
    
    def __lt__(self, __o: object) -> bool:
        if not isinstance(__o, Resources):
            raise NotImplemented('Not implemented')
        return all(getattr(self, resource_type) < getattr(__o, resource_type) for resource_type in self.__dict__)
    
    def __ge__(self, __o: object) -> bool:
        if not isinstance(__o, Resources):
            raise NotImplemented('Not implemented')
        return all(getattr(self, resource_type) >= getattr(__o, resource_type) for resource_type in self.__dict__)
    
    def copy(self) -> 'Resources':
        return Resources(**self.__dict__)
    
    def __sub__(self, __o: object) -> 'Resources':
        if not isinstance(__o, Resources):
            return NotImplemented
        return Resources(**{resource_type: getattr(self, resource_type) - getattr(__o, resource_type) for resource_type in self.__dict__})

    def __add__(self, __o: object) -> 'Resources':
        if not isinstance(__o, Resources):
            return NotImplemented
        return Resources(**{resource_type: getattr(self, resource_type) + getattr(__o, resource_type) for resource_type in self.__dict__})
    
    def __getitem__(self, __o: object) -> int:
        if not isinstance(__o, str):
            return NotImplemented
        return getattr(self, __o)
    
    def __setitem__(self, __o: object, __v: object) -> None:
        if not isinstance(__o, str):
            return NotImplemented
        setattr(self, __o, __v)
    


@dataclass
class Blueprint(object):
    id: int 
    ore_bot_cost: 'Resources' 
    clay_bot_cost: 'Resources'
    obsidian_bot_cost: 'Resources'
    geode_bot_cost: 'Resources'

    @staticmethod
    def from_string(bluepring_string: str) -> 'Blueprint':
        bluepring_string = bluepring_string.replace('Blueprint ', '')
        id_part, the_rest = bluepring_string.split(': ')
        id = int(id_part)
        the_rest = the_rest.replace('Each ', '').replace('ore robot ', '').replace('clay robot ', '').replace('obsidian robot ', '').replace('geode robot ', '').replace('costs ', '').strip('.')
        bot_cost_parts = the_rest.split('. ')
        bot_costs = {}
        for bot_cost_part, bot_type in zip(bot_cost_parts, ['ore', 'clay', 'obsidian', 'geode']):
            bot_resource_costs = bot_cost_part.split(' and ')
            costs = {}
            for bot_resource_cost in bot_resource_costs:
                bot_resource_cost = bot_resource_cost.split(' ')
                costs[bot_resource_cost[1]] = int(bot_resource_cost[0])
            
            bot_costs[f'{bot_type}_bot_cost'] = Resources(**costs)
        
        return Blueprint(id, **bot_costs)

    def __getitem__(self, __o: object) -> 'Resources':
        if not isinstance(__o, str):
            return NotImplemented
        return getattr(self, f'{__o}_bot_cost')

    def __setitem__(self, __o: object, __v: object) -> None:
        if not isinstance(__o, str):
            return NotImplemented
        setattr(self, f'{__o}_bot_cost', __v)

    
def find_max_geodes(
    blueprint: 'Blueprint', 
    time_limit: int=24, 
    current_time: int=0, 
    resources: Optional['Resources']=None, 
    bots: Optional[Dict[str, int]]=None,
    passed_bots: Optional[List[str]]=None
) -> int:

    if resources is None:
        resources = Resources(0, 0, 0, 0)
    if bots is None:
        bots = {'ore': 1, 'clay': 0, 'obsidian': 0, 'geode': 0}
    if passed_bots is None:
        passed_bots = []

    if current_time >= time_limit and resources.geode >= 9:
        print(f'Current time: {current_time} - Resources: {resources} - Bots: {bots}')
 
    current_time += 1
    
    while current_time <= time_limit:
     
        # Figure out what robots I can build
        bots_we_can_build = []
        for bot_type in bots:
            if resources >= blueprint[bot_type]:
                bots_we_can_build.append(bot_type)

        # Harvest resources w/ existing bots
        for bot_type in bots:
            resources[bot_type] = resources[bot_type] + bots[bot_type]

        if bots_we_can_build:

            max_geodes = resources.geode
            if 'geode' in bots_we_can_build:
                test_bots_we_can_build = ['geode']
            else:
                test_bots_we_can_build = list(set(bots_we_can_build).difference(set(passed_bots))) + ['']

            for bot_type in test_bots_we_can_build:
                test_bots = {**bots}
                test_resources = resources.copy()
                
                if bot_type != '':
                    test_bots[bot_type] += 1
                    test_resources = test_resources - blueprint[bot_type]
                    passed_bots = []
                else:
                    passed_bots = bots_we_can_build.copy()
                
                test_geodes = find_max_geodes(blueprint, time_limit, current_time, test_resources, test_bots, passed_bots)
                if test_geodes > max_geodes:
                    max_geodes = test_geodes
            
            current_time = time_limit

            resources.geode = max_geodes
        
        current_time += 1   
        
    return resources.geode


def total_quality_level(blueprints: List['Blueprint'], time_limit: int=24) -> int:
    return sum(blueprint.id * find_max_geodes(blueprint, time_limit) for blueprint in blueprints)


if __name__ == '__main__':
    ### THE TESTS
    test_input = '''Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian.'''.split('\n')

    test_blueprints = [Blueprint.from_string(blueprint) for blueprint in test_input]
    assert Resources(2, 2, 3, 4) >= Resources(1, 2, 3, 4)
    assert find_max_geodes(test_blueprints[0]) == 9
    assert find_max_geodes(test_blueprints[1]) == 12
    assert total_quality_level(test_blueprints) == 33

    ### THE REAL THING
    puzzle_input = helper.read_input_lines()
    blueprints = [Blueprint.from_string(blueprint) for blueprint in puzzle_input]
    print(f'Part 1: {""}')
    print(f'Part 2: {""}')
