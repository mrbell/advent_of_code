from typing import List, Union
import sys    
import os    


calling_file_name = os.path.basename(sys.argv[0])
calling_file_path = os.path.dirname(os.path.abspath(sys.argv[0]))
puzzle_day = int(calling_file_name.replace('day', '').replace('.py', ''))


def read_input(day_num: Union[int, None]=None) -> str:
    if not day_num:
        day_num = puzzle_day
    with open(os.path.join(calling_file_path, './inputs/day{:>02}.txt'.format(day_num)), 'r') as f:
        contents = f.read()
    return contents.strip()

def read_input_lines(day_num: Union[int, None]=None) -> List[str]:
    if not day_num:
        day_num = puzzle_day
    contents = read_input(day_num)
    return [c for c in contents.split('\n') if c.strip()]
