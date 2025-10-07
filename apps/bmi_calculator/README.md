# BMI Calculator (Python)

A simple Python module for calculating Body Mass Index (BMI) along with a
weight classification based on World Health Organization guidelines.

## Usage

```python
from apps.bmi_calculator import bmi

result = bmi.calculate_bmi(weight_kg=68, height_m=1.75)
print(result.bmi, result.category)
```

## Running Tests

```bash
python -m pytest apps/bmi_calculator
```
