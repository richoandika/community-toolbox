# Tip Calculator

A lightweight Python command-line tool that helps you calculate restaurant tips and split bills between friends in seconds.

## Features

- Calculates tip amount and total cost based on a percentage you choose
- Splits the bill evenly across any number of people
- Optional rounding so everyone pays the same amount to the nearest cent
- Includes a reusable module for other Python projects

## Getting Started

```bash
python tip_calculator.py 85.40 --tip 18 --people 3 --round
```

This command will output a neatly formatted breakdown showing the tip, total, and per-person amounts. Use `--help` to see all options.

## Running Tests

```bash
pytest apps/tip-calculator/tests
```
