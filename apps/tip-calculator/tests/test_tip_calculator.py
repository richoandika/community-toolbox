"""Tests for the tip calculator module."""

from __future__ import annotations

import math
import os
import sys
from decimal import Decimal

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tip_calculator import (
    TipBreakdown,
    calculate_tip,
    calculate_tip_from_cli,
    format_breakdown,
    main,
    parse_arguments,
)


@pytest.mark.parametrize(
    "bill, tip, num_people, expected_tip, expected_total, expected_per_person",
    [
        (100, 20, 1, Decimal("20.00"), Decimal("120.00"), Decimal("120.00")),
        (80, 18, 4, Decimal("14.40"), Decimal("94.40"), Decimal("23.60")),
        (53.27, 18, 3, Decimal("9.59"), Decimal("62.86"), Decimal("20.95")),
    ],
)
def test_calculate_tip(bill, tip, num_people, expected_tip, expected_total, expected_per_person):
    breakdown = calculate_tip(bill, tip, num_people=num_people)

    assert isinstance(breakdown, TipBreakdown)
    assert breakdown.tip_amount == expected_tip
    assert breakdown.total_amount == expected_total
    assert breakdown.amount_per_person == expected_per_person


def test_calculate_tip_round_up_adjusts_total():
    breakdown = calculate_tip(53.27, 18, num_people=3, round_up=True)

    assert breakdown.amount_per_person == Decimal("20.96")
    assert breakdown.total_amount == Decimal("62.88")
    assert math.isclose(float(breakdown.tip_amount), 9.61, abs_tol=0.01)


@pytest.mark.parametrize(
    "bill, tip, people, expected_message",
    [
        (-10, 15, 1, "bill_amount"),
        (10, -5, 1, "tip_percent"),
        (10, 15, 0, "num_people"),
    ],
)
def test_calculate_tip_invalid_inputs(bill, tip, people, expected_message):
    with pytest.raises(ValueError) as excinfo:
        calculate_tip(bill, tip, num_people=people)

    assert expected_message in str(excinfo.value)


def test_format_breakdown_output_custom_currency():
    breakdown = calculate_tip(45.5, 22, num_people=2)
    output = format_breakdown(breakdown, currency_symbol="€")

    assert "Bill Amount: €45.50" in output
    assert "Tip Percentage: 22.00%" in output
    assert output.endswith("Amount Per Person: €27.76")


def test_calculate_tip_from_cli_arguments_rounding():
    args = {"bill": "75.5", "tip": "18", "people": "3", "round": "true"}
    breakdown = calculate_tip_from_cli(args)

    assert breakdown.num_people == 3
    assert math.isclose(float(breakdown.tip_amount), 13.59, abs_tol=0.01)


def test_parse_arguments_and_main_execution(capsys):
    namespace = parse_arguments(["100", "--tip", "25", "--people", "4", "--currency", "£"])

    assert namespace.bill == 100.0
    assert namespace.tip == 25.0
    assert namespace.people == 4
    assert namespace.currency == "£"

    exit_code = main(["100", "--tip", "25", "--people", "4", "--currency", "£"])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "Bill Amount: £100.00" in captured.out
    assert "Tip Amount:" in captured.out
