"""Simple tip calculator module."""
from dataclasses import dataclass
from decimal import Decimal, ROUND_CEILING, ROUND_HALF_UP
from typing import Dict


@dataclass(frozen=True)
class TipBreakdown:
    """Represents calculated tip information."""

    bill_amount: float
    tip_percent: float
    num_people: int
    tip_amount: float
    total_amount: float
    amount_per_person: float


def calculate_tip(
    bill_amount: float,
    tip_percent: float,
    num_people: int = 1,
    round_up: bool = False,
) -> TipBreakdown:
    """Calculate tip and totals.

    Args:
        bill_amount: Original bill before tip.
        tip_percent: Tip percentage (e.g. 20 for 20%).
        num_people: How many people split the bill.
        round_up: Whether to round the per-person amount up to the nearest cent.

    Returns:
        TipBreakdown containing calculation results.

    Raises:
        ValueError: If inputs are invalid.
    """

    if bill_amount < 0:
        raise ValueError("bill_amount must be non-negative")
    if tip_percent < 0:
        raise ValueError("tip_percent must be non-negative")
    if num_people <= 0:
        raise ValueError("num_people must be greater than zero")

    bill = Decimal(str(bill_amount)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    tip_pct = Decimal(str(tip_percent))

    tip_amount = (bill * tip_pct / Decimal("100")).quantize(
        Decimal("0.01"), rounding=ROUND_HALF_UP
    )
    total_amount = (bill + tip_amount).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    if round_up:
        amount_per_person = (total_amount / num_people).quantize(
            Decimal("0.01"), rounding=ROUND_CEILING
        )
        total_amount = (amount_per_person * num_people).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )
        tip_amount = (total_amount - bill).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )
    else:
        amount_per_person = (total_amount / num_people).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )

    return TipBreakdown(
        bill_amount=float(bill),
        tip_percent=float(tip_percent),
        num_people=num_people,
        tip_amount=float(tip_amount),
        total_amount=float(total_amount),
        amount_per_person=float(amount_per_person),
    )


def format_breakdown(breakdown: TipBreakdown) -> str:
    """Format a tip breakdown for display."""

    return (
        f"Bill Amount: ${breakdown.bill_amount:.2f}\n"
        f"Tip Percentage: {breakdown.tip_percent:.1f}%\n"
        f"Number of People: {breakdown.num_people}\n"
        f"Tip Amount: ${breakdown.tip_amount:.2f}\n"
        f"Total Amount: ${breakdown.total_amount:.2f}\n"
        f"Amount Per Person: ${breakdown.amount_per_person:.2f}"
    )


def calculate_tip_from_cli(args: Dict[str, str]) -> TipBreakdown:
    """Helper to calculate tip using CLI-style arguments."""

    bill_amount = float(args.get("bill", 0))
    tip_percent = float(args.get("tip", 20))
    num_people = int(args.get("people", 1))
    round_up = args.get("round", "false").lower() in {"true", "1", "yes", "y"}

    return calculate_tip(bill_amount, tip_percent, num_people, round_up)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Calculate restaurant tips with ease.")
    parser.add_argument("bill", type=float, help="Bill amount before tip")
    parser.add_argument(
        "--tip",
        type=float,
        default=20,
        help="Tip percentage to apply (default: 20)",
    )
    parser.add_argument(
        "--people",
        type=int,
        default=1,
        help="Number of people splitting the bill (default: 1)",
    )
    parser.add_argument(
        "--round",
        action="store_true",
        help="Round up the per-person amount to the nearest cent",
    )

    parsed_args = parser.parse_args()

    breakdown = calculate_tip(
        bill_amount=parsed_args.bill,
        tip_percent=parsed_args.tip,
        num_people=parsed_args.people,
        round_up=parsed_args.round,
    )

    print(format_breakdown(breakdown))
