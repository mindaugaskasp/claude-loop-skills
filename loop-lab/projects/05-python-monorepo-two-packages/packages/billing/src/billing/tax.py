from decimal import ROUND_HALF_UP, Decimal

RATES: dict[str, Decimal] = {
    "LT": Decimal("0.21"),
    "LV": Decimal("0.21"),
    "EE": Decimal("0.22"),
    "DE": Decimal("0.19"),
}


class UnknownCountryError(ValueError):
    pass


def tax_for(net: Decimal, country: str) -> Decimal:
    try:
        rate = RATES[country.upper()]
    except KeyError as exc:
        raise UnknownCountryError(f"no tax rate for {country!r}") from exc
    return (net * rate).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
