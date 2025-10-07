import math

import pytest

from apps.bmi_calculator import bmi


def test_calculate_bmi_normal_weight():
    result = bmi.calculate_bmi(68, 1.75)
    assert math.isclose(result.bmi, 22.2, abs_tol=0.1)
    assert result.category == "Normal weight"


def test_calculate_bmi_underweight():
    result = bmi.calculate_bmi(45, 1.7)
    assert result.category == "Underweight"


def test_calculate_bmi_obesity():
    result = bmi.calculate_bmi(120, 1.7)
    assert result.category == "Obesity"


def test_calculate_bmi_invalid_inputs():
    with pytest.raises(ValueError):
        bmi.calculate_bmi(-60, 1.8)
    with pytest.raises(ValueError):
        bmi.calculate_bmi(60, 0)
