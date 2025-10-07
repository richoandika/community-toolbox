"""BMI Calculator module."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class BMIResult:
    bmi: float
    category: str


def calculate_bmi(weight_kg: float, height_m: float) -> BMIResult:
    """Calculate BMI and return the numeric value and classification."""
    if height_m <= 0:
        raise ValueError("height must be greater than zero")
    if weight_kg <= 0:
        raise ValueError("weight must be greater than zero")

    bmi = weight_kg / (height_m ** 2)
    category = classify_bmi(bmi)
    return BMIResult(bmi=round(bmi, 1), category=category)


def classify_bmi(bmi: float) -> str:
    """Classify BMI into WHO categories."""
    if bmi < 18.5:
        return "Underweight"
    if bmi < 25:
        return "Normal weight"
    if bmi < 30:
        return "Overweight"
    return "Obesity"
