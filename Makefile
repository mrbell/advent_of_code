PHONY=init run

# Optional parameters; defaults: YEAR=current year, DAY=current day
YEAR?=$(shell date +%Y)
DAY?=$(shell date +%d)

# Ensure day is zero-padded when provided as single digit (e.g., DAY=9)
DAY2:=$(if $(filter 1 2 3 4 5 6 7 8 9,$(DAY)),0$(DAY),$(DAY))

# Initialize AoC files for given day/year
init:
	uv run python aoc.py init $(if $(DAY2),-d $(DAY2)) $(if $(YEAR),-y $(YEAR))

# Run the solution script for given day/year
run:
	uv run python $(YEAR)/day$(DAY2).py

