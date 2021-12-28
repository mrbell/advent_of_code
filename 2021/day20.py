from __future__ import annotations
from dataclasses import dataclass
from typing import List, Tuple
import helper
from day03 import bin2dec


pixel_map = {'.': 0, '#': 1}
inv_pixel_map = {pixel_map[k]: k for k in pixel_map}


@dataclass
class Image:
    bitmap: List[List[int]]
    enhancement_alg: EnhancementAlgorithm
    bg_val: int=0

    def pad(self, n: int=2, pad_val: int=0) -> None:
        padded_rows = len(self.bitmap) + 2*n
        padded_cols = len(self.bitmap[0]) + 2*n

        new_bitmap = [[pad_val] * padded_cols for _ in range(padded_rows)]
        for row_num, row in enumerate(self.bitmap):
            for col_num, val in enumerate(row):
                new_bitmap[n+row_num][n+col_num] = val
        self.bitmap = new_bitmap
    
    def trim(self) -> None:
        min_row = len(self.bitmap)
        for row_num, row in enumerate(self.bitmap):
            if sum(row) > 0:
                min_row = row_num 
                break
        max_row = 0
        for row_num, row in enumerate(self.bitmap[::-1]):
            if sum(row) > 0:
                max_row = len(self.bitmap) - row_num
                break
        min_col = len(self.bitmap[0])
        for col_num in range(len(self.bitmap[0])):
            if sum(row[col_num] for row in self.bitmap) > 0:
                min_col = col_num
                break

        max_col = 0
        for col_num in range(len(self.bitmap[0])-1, -1, -1):
            if sum(row[col_num] for row in self.bitmap) > 0:
                max_col = col_num + 1
                break
        
        new_bitmap = []
        for row in self.bitmap[min_row:max_row]:
            new_bitmap.append(row[min_col:max_col])
        self.bitmap = new_bitmap
                
    def __str__(self) -> str:
        im_str_rows = []
        for row in self.bitmap:
            im_str_rows.append(
                ''.join([inv_pixel_map[v] for v in row])
            )
        return '\n'.join(im_str_rows)

    def get_lookup_code(self, row_num: int, col_num: int) -> int:
        bin_code = ''
        for chip_row_num in range(row_num - 1, row_num + 2):
            for chip_col_num in range(col_num - 1, col_num + 2):
                bin_code += str(self.bitmap[chip_row_num][chip_col_num])
        return bin2dec(bin_code)
 
    def enhanced_pixel(self, row_num: int, col_num: int) -> int:
        bin_code = self.get_lookup_code(row_num, col_num)
        return self.enhancement_alg[bin_code]

    def enhance(self) -> Image:
        bg_val = self.bg_val
        self.pad(pad_val=bg_val)
        new_bg_val = self.enhancement_alg[0] if bg_val == 0 else self.enhancement_alg[-1]
        new_bitmap = [[new_bg_val] * len(self.bitmap[0]) for _ in range(len(self.bitmap))]
        for row_num in range(1, len(self.bitmap) - 1):
            for col_num in range(1, len(self.bitmap[0]) - 1):
                new_bitmap[row_num][col_num] = self.enhanced_pixel(row_num, col_num)
        new_image = Image(new_bitmap, self.enhancement_alg, new_bg_val)
        new_image.trim()
        return new_image
    
    def count_lit_pixels(self) -> int:
        counter = 0
        for row in self.bitmap:
            for val in row:
                counter += val
        return counter


@dataclass
class EnhancementAlgorithm:
    lookup_table: List[int]

    def __getitem__(self, index: int) -> int:
        return self.lookup_table[index]


def input_parser(input_str: str) -> Image:
    alg_str, image_str = input_str.strip().split('\n\n')
    enhancement_alg = EnhancementAlgorithm([pixel_map[val] for val in alg_str])
    image_str = image_str.strip().split('\n')
    bitmap = [[pixel_map[val] for val in row] for row in image_str]
    image = Image(bitmap, enhancement_alg)
    return image
    

if __name__ == '__main__':
    ### THE TESTS
    test_input = '''..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..###..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#..#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#......#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.......##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

#..#.
#....
##..#
..#..
..###'''

    test_image = input_parser(test_input)

    assert test_image.get_lookup_code(2, 2) == 34
    assert test_image.enhanced_pixel(2, 2) == 1

    print(test_image, end='\n\n')
    test_image.pad()
    print(test_image, end='\n\n')
    test_image.trim()
    print(test_image, end='\n\n')

    enhanced_image = test_image.enhance()
    print(enhanced_image, end='\n\n')

    enhanced_image = enhanced_image.enhance()
    print(enhanced_image, end='\n\n')

    assert enhanced_image.count_lit_pixels() == 35

    for _ in range(48):
        enhanced_image = enhanced_image.enhance()
    
    assert enhanced_image.count_lit_pixels() == 3351
    
    ### THE REAL THING
    puzzle_input = helper.read_input()
    image = input_parser(puzzle_input)
    print(image, end='\n\n')
    enhanced_image = image.enhance().enhance()
    print(enhanced_image, end='\n\n')
    print(f'Part 1: {enhanced_image.count_lit_pixels()}')

    for i in range(48):
        enhanced_image = enhanced_image.enhance()
        if (i + 2) % 5 == 0:
            print(str(i+2), end=' ')
    print()

    print(f'Part 2: {enhanced_image.count_lit_pixels()}')
