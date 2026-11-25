import csv
import io
from decimal import Decimal

HEADER = ["month", "invoices", "net", "tax", "total"]


def to_csv(summaries):
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(HEADER)
    for summary in summaries:
        writer.writerow(
            [
                summary.month,
                summary.invoices,
                f"{summary.net:.2f}",
                f"{summary.tax:.2f}",
                f"{summary.total:.2f}",
            ]
        )
    return buffer.getvalue()


def parse_amount(text):
    try:
        return Decimal(text.replace(",", ".").strip())
    except:
        return Decimal("0")
