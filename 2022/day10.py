from typing import List, Optional 
import helper


class CRT(object):
    DARK = '.'
    LIGHT = '#'

    def __init__(self, rows: int=6, cols: int=40):
        self.rows = rows
        self.cols = cols
        self.grid = [['.' for _ in range(cols)] for _ in range(rows)]

    def draw(self, cycle: int, sprite_location: int):
        position = (cycle - 1) % (self.rows * self.cols)
        pos_col = position % self.cols
        pos_row = position // self.cols

        if (sprite_location - 1) <= pos_col <= (sprite_location + 1):
            self.grid[pos_row][pos_col] = CRT.LIGHT

    def display(self):
        for row in self.grid:
            print(''.join(row))


class CPU(object):
    def __init__(self):
        self.register = 1
        self.cycle = 0
    
    def run(self, program: List[str], n_cycles:int = 240, crt: Optional[CRT]=None) -> int:
        current_op = 0
        executing_op = False
        execution_cycles = 0

        signal_strength = 0

        while self.cycle < n_cycles:
            self.cycle += 1
            op = program[current_op]

            if (self.cycle == 20) or ((self.cycle - 20) % 40 == 0):
                signal_strength += self.register * self.cycle
            
            if crt is not None:
                crt.draw(self.cycle, self.register)

            if not executing_op:
                if op.startswith('noop'):
                    current_op += 1
                elif op.startswith('addx'):
                    executing_op = True
                    execution_cycles += 1
                else:
                    raise ValueError(f'Unknown op: {op}')
            else:
                execution_cycles += 1

                if execution_cycles >= 2:
                    executing_op = False
                    execution_cycles = 0
                    self.register += int(
                        op.split(' ')[1]
                    )
                    current_op += 1

        return signal_strength


if __name__ == '__main__':
    ### THE TESTS
    small_test = '''noop
addx 3
addx -5'''.split('\n')
    cpu = CPU()
    _ = cpu.run(small_test, 5)
    assert cpu.register == -1

    larger_test = '''addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop'''.split('\n')
    cpu = CPU()
    crt = CRT()
    sig_strength = cpu.run(larger_test, 240, crt)
    assert sig_strength == 13140
    crt.display()

    ### THE REAL THING
    puzzle_input = helper.read_input_lines()
    cpu = CPU()
    crt = CRT()
    sig_strength = cpu.run(puzzle_input, 240, crt)
    print(f'Part 1: {sig_strength}')
    print(f'Part 2: See CRT output below')
    crt.display()
