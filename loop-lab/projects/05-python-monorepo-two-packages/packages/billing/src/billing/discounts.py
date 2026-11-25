from decimal import Decimal

KNOWN_CODES: dict[str, Decimal] = {
    "WELCOME10": Decimal("0.10"),
    "YEARLY15": Decimal("0.15"),
    "PARTNER25": Decimal("0.25"),
}

MAX_DISCOUNT = Decimal("0.30")


def discount_rate(codes: list[str], extra: dict[str, Decimal] = {}) -> Decimal:
    table = {**KNOWN_CODES, **extra}
    rate = sum((table[code] for code in codes if code in table), Decimal("0"))
    return min(rate, MAX_DISCOUNT)


def apply_discounts(amount: Decimal, codes: list[str]) -> Decimal:
    rate = discount_rate(codes)
    return (amount * (Decimal("1") - rate)).quantize(Decimal("0.01"))
