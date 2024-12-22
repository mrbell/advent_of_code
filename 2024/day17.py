from typing import List, Tuple, Dict
import helper


opcodes = ['adv', 'bxl', 'bst', 'jnz', 'bxz', 'out', 'bdv', 'cdv']


class ThreeBitComputer(object):
    def __init__(self, program: List[int], registers: Dict[str, int]):
        self.program = program
        self.registers = registers
        self.pointer = 0
        self.output = []

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


def part2(puzzle_input: str) -> int:
    Areg = 1
    while True:
        computer = parse(puzzle_input)
        computer.registers['A'] = Areg
        if computer.run() == ','.join(map(str, computer.program)):
            return Areg
        Areg += 1
        if Areg % 1000 == 0:
            print(Areg)


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
    helper.check(part2(example_input), 117440)


    ### THE REAL THING
    puzzle_input = helper.read_input()
    print(f'Part 1: {part1(puzzle_input)}')
    print(f'Part 2: {part2(puzzle_input)}')
