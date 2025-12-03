PHONY=init run

# Optional parameters; defaults: YEAR=current year, DAY=current day
YEAR?=$(shell date +%Y)
DAY?=$(shell date +%d)

# Initialize AoC files for given day/year
init:
	uv run python aoc.py init $(if $(DAY),-d $(DAY)) $(if $(YEAR),-y $(YEAR))

# Run the solution script for given day/year
run:
	uv run python $(YEAR)/day$(shell printf "%02d" $(DAY)).py

