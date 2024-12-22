from typing import List, Tuple, Dict
import helper


opcodes = ['adv', 'bxl', 'bst', 'jnz', 'bxz', 'out', 'bdv', 'cdv']


class ThreeBitComputer(object):
    def __init__(self, program: List[int], registers: Dict[str, int]):
        self.program = program
        self.registers = registers
        self.pointer = 0
        self.output = []
    
    def print_program(self):
        print(','.join(list(map(str, self.program))))
    
    def print_output(self):
        print(','.join(list(map(str, self.output))))

    def combo(self, operand):
        if operand <= 3: 
            return operand
        elif operand == 7:
            raise ValueError('Invalid operand')
        elif operand == 4:
            return self.registers['A']
        elif operand == 5:
            return self.registers['B']
        elif operand == 6:
            return self.registers['C']
        else:
            raise ValueError('Invalid operand')

    def adv(self, operand):
        # Opcode 0
        num = self.registers['A']
        den = 2 ** self.combo(operand)
        self.registers['A'] = num // den
        return 2

    def bxl(self, operand):
        # Opcode 1
        self.registers['B'] = self.registers['B'] ^ operand
        return 2

    def bst(self, operand):
        # Opcode 2
        self.registers['B'] = self.combo(operand) % 8
        return 2
    
    def jnz(self, operand):
        # Opcode 3
        if self.registers['A'] != 0:
            self.pointer = operand
            return 0
        return 2
            
    def bxz(self, operand):
        # Opcode 4
        self.registers['B'] = self.registers['B'] ^ self.registers['C']
        return 2
    
    def out(self, operand):
        # Opcode 5
        self.output.append(self.combo(operand) % 8)
        return 2
    
    def bdv(self, operand):
        # Opcode 6
        num = self.registers['A']
        den = 2 ** self.combo(operand)
        self.registers['B'] = num // den
        return 2
    
    def cdv(self, operand):
        # Opcode 7
        num = self.registers['A']
        den = 2 ** self.combo(operand)
        self.registers['C'] = num // den
        return 2

    def run(self):
        while self.pointer < len(self.program):
            opcode = self.program[self.pointer]
            operand = self.program[self.pointer + 1]
            jmp = getattr(self, opcodes[opcode])(operand)
            self.pointer += jmp
        return ','.join(list(map(str, self.output)))


def parse_register_line(reg_line: str) -> Tuple[str, int]:
    reg_name, reg_val = reg_line.split(': ')
    return reg_name.replace('Register ', ''), int(reg_val)


def parse(comp_def: str) -> ThreeBitComputer:
    registers, program = comp_def.split('\n\n')
    registers = {rl[0]: rl[1] for rl in map(parse_register_line, registers.split('\n'))}
    program = list(map(int, program.replace('Program: ', '').split(',')))

    return ThreeBitComputer(program, registers)


def part1(puzzle_input: str) -> str:
    computer = parse(puzzle_input)
    return computer.run()


def find_output_lower(puzzle_input: str) -> int:
    Areg = 1
    Areg_lower = None
    Areg_upper = None
    while Areg_lower is None or Areg_upper is None:
        computer = parse(puzzle_input)
        computer.registers['A'] = Areg
        result = computer.run()
        if len(computer.output) < len(computer.program):
            if Areg_lower is None:
                Areg_lower = Areg
            elif Areg > Areg_lower:
                Areg_lower = Areg
            Areg *= 2 ** (len(computer.program) - len(computer.output))
        elif len(computer.output) >= len(computer.program):
            if Areg_upper is None:
                Areg_upper = Areg
            elif Areg < Areg_upper:
                Areg_upper = Areg
            Areg = Areg // 2
    
    while True:
        Areg = (Areg_lower + Areg_upper) // 2
        computer = parse(puzzle_input)
        computer.registers['A'] = Areg
        result = computer.run()
        if len(computer.output) < len(computer.program):
            other_computer = parse(puzzle_input)
            other_computer.registers['A'] = Areg + 1
            other_result = other_computer.run()
            if len(other_computer.output) == len(computer.program):
                return Areg + 1
            Areg_lower = Areg
        elif len(computer.output) > len(computer.program):
            Areg_upper = Areg
        else:
            other_computer = parse(puzzle_input)
            other_computer.registers['A'] = Areg - 1
            other_result = other_computer.run()
            if len(other_computer.output) < len(computer.program):
                return Areg
            Areg_upper = Areg




def find_output_upper(puzzle_input: str) -> int:
    Areg = 1
    Areg_lower = None
    Areg_upper = None
    while Areg_lower is None or Areg_upper is None:
        computer = parse(puzzle_input)
        computer.registers['A'] = Areg
        result = computer.run()
        if len(computer.output) <= len(computer.program):
            if Areg_lower is None:
                Areg_lower = Areg
            elif Areg > Areg_lower:
                Areg_lower = Areg
            Areg *= 2 ** (len(computer.program) - len(computer.output) + 1)
        elif len(computer.output) > len(computer.program):
            if Areg_upper is None:
                Areg_upper = Areg
            elif Areg < Areg_upper:
                Areg_upper = Areg
            Areg = Areg // 2
    
    while True:
        Areg = (Areg_lower + Areg_upper) // 2
        computer = parse(puzzle_input)
        computer.registers['A'] = Areg
        result = computer.run()
        if len(computer.output) < len(computer.program):
            Areg_lower = Areg
        elif len(computer.output) > len(computer.program):
            Areg_upper = Areg
        else:
            other_computer = parse(puzzle_input)
            other_computer.registers['A'] = Areg + 1
            other_result = other_computer.run()
            if len(other_computer.output) > len(computer.program):
                return Areg
            Areg_lower = Areg



def part2(puzzle_input: str) -> int:
    '''
    Manually searched through as follows
    - Find the lower and upper A registers that produce the correct length of output
    - Split the range up into 200 parts
    - Find the A register just before and after the one that produces the correct last digit of the output
    - Search through the range of A registers between the two found above to find the range in which the next to last digit fallse within
    - Repeat until the lower to upper bounds are small enough to linear search


    I could automate this process, but it's not worth the time to do so right now
    Interesting as it's not a binary search because there isn't a monotonically increasing value to search over but kind of similar in concept
    '''

    lower_Areg = find_output_lower(puzzle_input)
    upper_Areg = find_output_upper(puzzle_input)
    lower_Areg = 190384609150581 
    upper_Areg = 190384613365317
    print(f'Lower: {lower_Areg},  Upper: {upper_Areg}')
    print(f'Range: {upper_Areg - lower_Areg}')
    print('-----------------')

    Aregs = range(lower_Areg, upper_Areg + 1)
    for Areg in Aregs:
        computer = parse(puzzle_input)
        computer.registers['A'] = Areg
        result = computer.run()
        if computer.output == computer.program:
            return Areg

    Aregs = range(lower_Areg, upper_Areg + 1, (upper_Areg - lower_Areg) // 200)
    for Areg in Aregs:
        computer = parse(puzzle_input)
        computer.registers['A'] = Areg
        result = computer.run()
        print(Areg, ':',result)

    computer.print_program()

    Areg = 1
    while True:
        computer = parse(puzzle_input)
        computer.registers['A'] = Areg
        result = computer.run()
        print(Areg, result)
        if result == ','.join(map(str, computer.program)):
            return Areg
        if len(computer.output) < len(computer.program):
            Areg *= 2 ** (len(computer.program) - len(computer.output))
        elif len(computer.output) > len(computer.program):
            Areg = Areg // 2
        else:
            n_dig = 0
            for i in range(len(computer.program), 0, -1):
                if computer.program[i-1] == computer.output[i-1]:
                    n_dig = i
                else:
                    break
            n_dig = len(computer.program) - n_dig
            Areg += 10 ** n_dig


if __name__ == '__main__':
    ### THE TESTS
    example_input = '''Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0'''
    assert part1(example_input) == '4,6,3,5,6,3,5,2,1,0'

    example_input = '''Register A: 2024
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0'''
    # helper.check(part2(example_input), 117440)


    ### THE REAL THING
    puzzle_input = helper.read_input()
    print(f'Part 1: {part1(puzzle_input)}')
    print(f'Part 2: {part2(puzzle_input)}')
