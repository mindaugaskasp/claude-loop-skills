from collections import defaultdict
from dataclasses import dataclass
from decimal import Decimal

from billing import Invoice


@dataclass(frozen=True)
class MonthSummary:
    month: str
    invoices: int
    net: Decimal
    tax: Decimal

    @property
    def total(self):
        return self.net + self.tax


def month_key(invoice):
    return invoice.issued.strftime("%Y-%m")


def summarise(invoices):
    grouped = defaultdict(list)
    for invoice in invoices:
        grouped[month_key(invoice)].append(invoice)

    result = []
    for month in sorted(grouped):
        batch = grouped[month]
        net = Decimal("0")
        tax = Decimal("0")
        for invoice in batch:
            try:
                net += invoice.net
                tax += invoice.tax
            except:
                continue
        result.append(MonthSummary(month, len(batch), net, tax))
    return result


def is_invoice(value):
    return isinstance(value, Invoice)
