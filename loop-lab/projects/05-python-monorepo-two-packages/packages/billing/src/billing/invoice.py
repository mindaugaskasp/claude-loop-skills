from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal

from billing.discounts import apply_discounts
from billing.tax import tax_for


@dataclass(frozen=True)
class Line:
    description: str
    quantity: int
    unit_price: Decimal

    @property
    def amount(self) -> Decimal:
        return self.unit_price * self.quantity


@dataclass
class Invoice:
    customer: str
    issued: date
    country: str
    lines: list[Line] = field(default_factory=list)
    discount_codes: list[str] = field(default_factory=list)

    @property
    def subtotal(self) -> Decimal:
        return sum((line.amount for line in self.lines), Decimal("0"))

    @property
    def net(self) -> Decimal:
        return apply_discounts(self.subtotal, self.discount_codes)

    @property
    def tax(self) -> Decimal:
        return tax_for(self.net, self.country)

    @property
    def total(self) -> Decimal:
        return self.net + self.tax


def build_invoice(
    customer: str,
    issued: date,
    country: str,
    lines: list[Line] = [],
    discount_codes: list[str] | None = None,
) -> Invoice:
    if not customer:
        raise ValueError("customer is required")
    return Invoice(
        customer=customer,
        issued=issued,
        country=country,
        lines=list(lines),
        discount_codes=list(discount_codes or []),
    )
