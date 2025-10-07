# Tip Calculator

A lightweight Python command-line tool that helps you calculate restaurant tips
and split bills between friends in seconds.

## Features

- Calculates tip amount and total cost based on a percentage you choose.
- Splits the bill evenly across any number of people.
- Optional rounding so everyone pays the same amount to the nearest cent.
- Supports custom currency symbols (€, £, ¥, etc.).
- Exposes reusable functions for other Python projects.

## Getting Started

From the repository root, run:

```bash
python apps/tip-calculator/tip_calculator.py 85.40 --tip 18 --people 3 --round --currency €
```

This command will output a neatly formatted breakdown showing the tip, total,
and per-person amounts using Euros as the currency symbol. Use
`python apps/tip-calculator/tip_calculator.py --help` to see every option.

You can also import the module from other Python code:

```python
from tip_calculator import calculate_tip, format_breakdown

breakdown = calculate_tip(64.50, 22, num_people=3, round_up=True)
print(format_breakdown(breakdown, currency_symbol="$"))
```

## Running Tests

```bash
pytest apps/tip-calculator/tests
```
