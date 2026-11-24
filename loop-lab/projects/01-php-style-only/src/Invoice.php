<?php

declare(strict_types=1);

namespace Acme\Invoicing;

final class Invoice
{
    /** @var InvoiceLine[] */
    private array $lines = [];

    public function __construct(
        public readonly string $number,
        public readonly string $customerId,
        public readonly string $currency,
    ) {
    }

    public function addLine(InvoiceLine $line): void
    {
        $this->lines[] = $line;
    }

    /** @return InvoiceLine[] */
    public function lines(): array
    {
        return $this->lines;
    }

    public function subtotal(): Money
    {
        $total = new Money(0, $this->currency);
        foreach ($this->lines as $line) {
            $total = $total->add($line->total());
        }

        return $total;
    }
}
