# Advent of Code 2025

Advent of Code 2025 solutions.

## Design

General:

- Standard libraries only, no external or internal libraries allowed.
- No major refactoring after solving the puzzle.
- If the comment was made after solving the puzzle, mark it as such.

Commits:

- `feat`: puzzle solutions.
- `refactor`: code changes outside of puzzles (`./run`).
- `chore`: other changes (`README.md`, `pyproject.toml`).

## Get started

The entrypoint for the puzzles is `./run` (`./run --help`).

```sh
git clone https://github.com/sakhezech/aoc2025
cd aoc2025
python3 -m venv .venv
source .venv/bin/activate
pip install '.[dev]'
fate check
```
