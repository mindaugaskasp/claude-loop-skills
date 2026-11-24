<?php

namespace Acme\Invoicing;

final class InvoiceLine
{
    public function __construct(
        public readonly string $description,
        public readonly Money $unitPrice,
        public readonly int $quantity,
        public readonly string $taxCode,
    ) {
    }

    public function total(): Money
    {
        return $this->unitPrice->multiply($this->quantity);
    }
}
