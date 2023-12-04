# Advent of Code
## My solutions for various years

This repository contains my solutions for Advent of Code across the years. I have tended to solve using Python, and particularly sticking to native Python without use of any non-standard packages (e.g. I try to avoid using Numpy, although it would make some of the solutions much easier).

I have created a cli to make it easier to set up input and py files for a new puzzle. 
- You must set the AOC_COOKIE environment variable (copy from your browsers developer console) (see e.g. [here](https://github.com/wimglenn/advent-of-code-wim/issues/1) for details on how to get it in the right format)
- Run `python aoc.py init` to download the input for the current day and create a base .py file
  - You can optionally specify the year and day using the options `-y` and `-d` respectively

NOTES:
- 2021 requires Python 3.10

I have consolidated from previous repositories that contained solutions for individual years.
- https://github.com/mrbell/aoc2019
- https://github.com/mrbell/aoc2018
- https://github.com/mrbell/aoc2017
