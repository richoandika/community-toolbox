"""Core logic for the tip calculator app."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, ROUND_CEILING, ROUND_HALF_UP
from typing import Mapping, Sequence


CENTS = Decimal("0.01")
DEFAULT_TIP_PERCENT = Decimal("20")

__all__ = [
    "TipBreakdown",
    "calculate_tip",
    "calculate_tip_from_cli",
    "format_breakdown",
    "parse_arguments",
    "main",
]


def _to_decimal(value: float | int | str | Decimal) -> Decimal:
    """Convert arbitrary numeric input into a :class:`~decimal.Decimal`."""

    if isinstance(value, Decimal):
        return value
    return Decimal(str(value))


def _quantize_currency(value: Decimal, rounding: str = ROUND_HALF_UP) -> Decimal:
    """Round a Decimal to the nearest cent using the provided rounding mode."""

    return value.quantize(CENTS, rounding=rounding)


@dataclass(frozen=True)
class TipBreakdown:
    """Represents calculated tip information using precise decimal values."""

    bill_amount: Decimal
    tip_percent: Decimal
    num_people: int
    tip_amount: Decimal
    total_amount: Decimal
    amount_per_person: Decimal

    def as_dict(self) -> dict[str, str]:
        """Return a serialisable representation of the calculation."""

        return {
            "bill_amount": f"{self.bill_amount:.2f}",
            "tip_percent": f"{self.tip_percent:.2f}",
            "num_people": str(self.num_people),
            "tip_amount": f"{self.tip_amount:.2f}",
            "total_amount": f"{self.total_amount:.2f}",
            "amount_per_person": f"{self.amount_per_person:.2f}",
        }


def calculate_tip(
    bill_amount: float | int | str | Decimal,
    tip_percent: float | int | str | Decimal,
    num_people: int = 1,
    *,
    round_up: bool = False,
) -> TipBreakdown:
    """Calculate the tip amount and per-person split.

    Args:
        bill_amount: Original bill before tip.
        tip_percent: Tip percentage (e.g. ``20`` for 20%).
        num_people: Number of people to split the bill with.
        round_up: Whether to round *up* the per-person amount, ensuring
            everyone pays the same number of cents.

    Returns:
        A :class:`TipBreakdown` with currency-safe ``Decimal`` values.

    Raises:
        ValueError: If any numeric input is negative or ``num_people`` is less
            than one.
    """

    bill = _to_decimal(bill_amount)
    tip_pct = _to_decimal(tip_percent)

    if bill < 0:
        raise ValueError("bill_amount must be non-negative")
    if tip_pct < 0:
        raise ValueError("tip_percent must be non-negative")
    if num_people <= 0:
        raise ValueError("num_people must be greater than zero")

    bill = _quantize_currency(bill)
    tip_pct = _quantize_currency(tip_pct)
    tip_amount = _quantize_currency(bill * tip_pct / Decimal("100"))
    total_amount = _quantize_currency(bill + tip_amount)

    if round_up:
        amount_per_person = _quantize_currency(
            total_amount / Decimal(num_people), rounding=ROUND_CEILING
        )
        total_amount = _quantize_currency(amount_per_person * num_people)
        tip_amount = _quantize_currency(total_amount - bill)
    else:
        amount_per_person = _quantize_currency(total_amount / Decimal(num_people))

    return TipBreakdown(
        bill_amount=bill,
        tip_percent=tip_pct,
        num_people=num_people,
        tip_amount=tip_amount,
        total_amount=total_amount,
        amount_per_person=amount_per_person,
    )


def format_breakdown(
    breakdown: TipBreakdown,
    *,
    currency_symbol: str = "$",
    lines: Sequence[str] | None = None,
) -> str:
    """Format a tip breakdown for display.

    Args:
        breakdown: Result of :func:`calculate_tip`.
        currency_symbol: Symbol to prefix currency values with.
        lines: Optional custom template allowing callers to control line order.

    Returns:
        A human-readable, multi-line string suitable for CLI output.
    """

    default_lines: Sequence[str] = (
        f"Bill Amount: {currency_symbol}{breakdown.bill_amount:.2f}",
        f"Tip Percentage: {breakdown.tip_percent:.2f}%",
        f"Number of People: {breakdown.num_people}",
        f"Tip Amount: {currency_symbol}{breakdown.tip_amount:.2f}",
        f"Total Amount: {currency_symbol}{breakdown.total_amount:.2f}",
        f"Amount Per Person: {currency_symbol}{breakdown.amount_per_person:.2f}",
    )

    output_lines = lines or default_lines
    return "\n".join(output_lines)


def calculate_tip_from_cli(args: Mapping[str, str]) -> TipBreakdown:
    """Helper to calculate tips from CLI-style key-value arguments."""

    bill_amount = args.get("bill", 0)
    tip_percent = args.get("tip", DEFAULT_TIP_PERCENT)
    num_people = int(args.get("people", 1))
    round_up = str(args.get("round", "false")).lower() in {"true", "1", "yes", "y"}

    return calculate_tip(bill_amount, tip_percent, num_people, round_up=round_up)


def parse_arguments(argv: Sequence[str] | None = None):
    """Parse command-line arguments and return an ``argparse`` namespace."""

    import argparse

    parser = argparse.ArgumentParser(description="Calculate restaurant tips with ease.")
    parser.add_argument("bill", type=float, help="Bill amount before tip")
    parser.add_argument(
        "--tip",
        type=float,
        default=float(DEFAULT_TIP_PERCENT),
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
    parser.add_argument(
        "--currency",
        default="$",
        help="Currency symbol to use when displaying amounts (default: $)",
    )

    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    """CLI entry point for the tip calculator."""

    args = parse_arguments(argv)
    breakdown = calculate_tip(
        bill_amount=args.bill,
        tip_percent=args.tip,
        num_people=args.people,
        round_up=args.round,
    )

    print(
        format_breakdown(
            breakdown,
            currency_symbol=args.currency,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
