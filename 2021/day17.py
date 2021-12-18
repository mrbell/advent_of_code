from dataclasses import dataclass
from typing import List, Tuple
from math import sqrt
import helper


@dataclass
class Probe:
    vx: int
    vy: int        
    x: int=0
    y: int=0
    
    def step(self):
        self.x += self.vx
        self.y += self.vy
        if self.vx > 0:
            self.vx -= 1
        elif self.vx < 0:
            self.vx += 1
        self.vy -= 1

    def in_bounds(self, x_min, x_max, y_min, y_max):
        return x_min <= self.x <= x_max and y_min <= self.y <= y_max


def parse_target_area(target_def):
    target_def = target_def.strip().replace('target area: x=', '').replace('y=', '')
    x_part, y_part = target_def.split(', ')
    x_min, x_max = [int(p) for p in x_part.split('..')]
    y_min, y_max = [int(p) for p in y_part.split('..')]
    return x_min, x_max, y_min, y_max


def get_vx_bounds(x_min, x_max):
    '''
    v_x has to fall within the range returned in 
    order to have a chance of hitting the target.

    To get this I wrote down the equation for x as a function of 
    the # of steps. At some point when vx goes to zero, x doesn't 
    change any longer. The min vx must at least get the probe to
    the left edge of the bounding box. The equation for x as a 
    function of step # is 
        x(s) = s(vx + 1) - s(s + 1) / 2 if x <= vx
        x(s) = (vx + 1) ** 2 - (vx + 1)(vx + 2) / 2 if x > vx
    Just solve for vx such that max(x) = the left edge of the bounding box.

    Use the fact that sum(k, 1, n) = n(n+1)/2
    
    The max vx is easier, it just can't be so fast that you 
    completely skip the bounding box in the first step.
    '''
    return int(sqrt(2 * x_min + 0.25)), x_max


def get_vy_bounds(y_min):
    '''
    To derive this I used the equation for y as a fn of step # s, 
        y(s) = s(vy + 1) - s(s+1)/2
    and the equation for vy as a function of step # s
        vy(s) = vy - (s - 1)
    If you shoot upward to start, the probe will return to y=0
    at step 
        s0 = 2vy + 1
    At the next step (s0 + 1) the velocity can't be going so fast that
    we completely overshoot the bounding box. This sets the max
    vy, i.e. the vy that makes it so y(s0 + 1) = the lower edge of the 
    bounding box. To get this I solved vy(s0 + 1) = y_lower for vy.

    The lowest allowable vy is one that just does not completely overshoot
    the bounding box in one step.
    '''
    return y_min, -y_min - 1


def get_max_height(vy):
    return (vy + 1) ** 2 - (vy + 1) * (vy + 2) / 2


def max_height_to_hit_target(y_min):
    _, vy_max = get_vy_bounds(y_min)
    return int(get_max_height(vy_max))


def find_valid_starting_velocities(x_min, x_max, y_min, y_max):
    vx_min, vx_max = get_vx_bounds(x_min, x_max)
    vy_min, vy_max = get_vy_bounds(y_min)

    valid_velocities = []

    for vx in range(vx_min, vx_max + 1):
        for vy in range(vy_min, vy_max + 1):
            probe = Probe(vx, vy)
            while True:
                probe.step()
                if probe.in_bounds(x_min, x_max, y_min, y_max):
                    valid_velocities.append((vx, vy))
                    break
                elif probe.y < y_min:
                    break
    return valid_velocities


if __name__ == '__main__':
    ### THE TESTS
    test_target_area = 'target area: x=20..30, y=-10..-5'
    x_min, x_max, y_min, y_max = parse_target_area(test_target_area)
    assert max_height_to_hit_target(y_min) == 45
    starting_velocities = find_valid_starting_velocities(x_min, x_max, y_min, y_max)
    assert len(starting_velocities) == 112

    ### THE REAL THING
    puzzle_input = helper.read_input()
    x_min, x_max, y_min, y_max = parse_target_area(puzzle_input)

    print(f'Part 1: {max_height_to_hit_target(y_min)}')

    valid_velocities = find_valid_starting_velocities(x_min, x_max, y_min, y_max)

    print(f'Part 2: {len(valid_velocities)}')
