from datetime import date
from decimal import Decimal

import pytest

from billing import Line, build_invoice
from billing.discounts import discount_rate
from billing.tax import UnknownCountryError, tax_for


def make_lines() -> list[Line]:
    return [
        Line("Team plan", 3, Decimal("20.00")),
        Line("Extra storage", 1, Decimal("5.50")),
    ]


def test_totals() -> None:
    invoice = build_invoice("Acme", date(2026, 9, 1), "LT", make_lines())
    assert invoice.subtotal == Decimal("65.50")
    assert invoice.tax == Decimal("13.76")
    assert invoice.total == Decimal("79.26")


def test_discount_is_capped() -> None:
    assert discount_rate(["YEARLY15", "PARTNER25"]) == Decimal("0.30")


def test_discount_applied_before_tax() -> None:
    invoice = build_invoice("Acme", date(2026, 9, 1), "DE", make_lines(), ["WELCOME10"])
    assert invoice.net == Decimal("58.95")
    assert invoice.tax == Decimal("11.20")


def test_customer_required() -> None:
    with pytest.raises(ValueError):
        build_invoice("", date(2026, 9, 1), "LT")


def test_unknown_country() -> None:
    with pytest.raises(UnknownCountryError):
        tax_for(Decimal("10"), "XX")
