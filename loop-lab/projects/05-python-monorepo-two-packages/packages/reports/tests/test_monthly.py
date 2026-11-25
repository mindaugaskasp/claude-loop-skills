from datetime import date
from decimal import Decimal

from billing import Line, build_invoice
from reports import summarise
from reports.export import parse_amount, to_csv


def invoice(day, country="LT", price="100.00"):
    return build_invoice("Acme", day, country, [Line("Plan", 1, Decimal(price))])


def test_groups_by_month():
    summaries = summarise(
        [
            invoice(date(2026, 9, 3)),
            invoice(date(2026, 9, 20)),
            invoice(date(2026, 10, 1), price="50.00"),
        ]
    )
    assert [s.month for s in summaries] == ["2026-09", "2026-10"]
    assert summaries[0].invoices == 2
    assert summaries[0].net == Decimal("200.00")
    assert summaries[1].total == Decimal("60.50")


def test_csv_has_header_and_rows():
    text = to_csv(summarise([invoice(date(2026, 9, 3))]))
    lines = text.strip().splitlines()
    assert lines[0] == "month,invoices,net,tax,total"
    assert lines[1] == "2026-09,1,100.00,21.00,121.00"


def test_parse_amount():
    assert parse_amount(" 12,50 ") == Decimal("12.50")
    assert parse_amount("n/a") == Decimal("0")
