<?php

declare(strict_types=1);

namespace Acme\Invoicing;

final class Money
{
    public function __construct(
        public readonly int $cents,
        public readonly string $currency,
    ) {
    }

    public function add(Money $other): Money
    {
        return new Money($this->cents + $other->cents, $this->currency);
    }

    public function multiply(int $quantity): Money
    {
        return new Money($this->cents * $quantity, $this->currency);
    }

    public function format(): string
    {
        return sprintf('%s %d.%02d', $this->currency, intdiv($this->cents, 100), $this->cents % 100);
    }
}
