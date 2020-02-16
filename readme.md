# Killer sudoku solver

## Summary

Solver for Killer sudokus, details [here](https://en.wikipedia.org/wiki/Killer_sudoku).

Uses *PuLP* optimization library, details [here](https://pythonhosted.org/PuLP/)

WIP - get puzzle-sovler working that doesn't rely on external optimization libraries

Includes scraper and parser for dailykillersudoku.com, puzzles [here](https://www.dailykillersudoku.com)

## Dependencies

```bash
pip install pulp
pip install numpy
```

## Run tests 

```bash
pytest .
```

## Run code

```bash
python3 killer_client.py
```
