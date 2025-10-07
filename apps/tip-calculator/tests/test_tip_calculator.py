"""Tests for the tip calculator module."""

import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tip_calculator import TipBreakdown, calculate_tip, calculate_tip_from_cli, format_breakdown


def test_calculate_tip_basic():
    breakdown = calculate_tip(100, 20)

    assert isinstance(breakdown, TipBreakdown)
    assert breakdown.tip_amount == 20
    assert breakdown.total_amount == 120
    assert breakdown.amount_per_person == 120


def test_calculate_tip_split_evenly():
    breakdown = calculate_tip(80, 18, num_people=4)

    assert breakdown.tip_amount == 14.4
    assert breakdown.total_amount == 94.4
    assert breakdown.amount_per_person == 23.6


def test_calculate_tip_round_up():
    breakdown = calculate_tip(53.27, 18, num_people=3, round_up=True)

    assert math.isclose(breakdown.amount_per_person, 20.96)
    assert math.isclose(breakdown.total_amount, 62.88)
    assert math.isclose(breakdown.tip_amount, 9.61, abs_tol=0.01)


def test_calculate_tip_invalid_inputs():
    invalid_args = [
        (-10, 15, 1),
        (10, -5, 1),
        (10, 15, 0),
    ]

    for bill, tip, people in invalid_args:
        try:
            calculate_tip(bill, tip, people)
            raise AssertionError("Expected ValueError")
        except ValueError:
            pass


def test_format_breakdown_output():
    breakdown = calculate_tip(45.5, 22, num_people=2)
    output = format_breakdown(breakdown)

    assert "Bill Amount: $45.50" in output
    assert "Tip Percentage: 22.0%" in output
    assert "Number of People: 2" in output
    assert "Tip Amount: $10.01" in output
    assert "Total Amount: $55.51" in output
    assert "Amount Per Person: $27.76" in output


def test_calculate_tip_from_cli_arguments():
    args = {"bill": "75.5", "tip": "18", "people": "3", "round": "true"}
    breakdown = calculate_tip_from_cli(args)

    assert breakdown.num_people == 3
    assert math.isclose(breakdown.tip_amount, 13.59, abs_tol=0.01)


