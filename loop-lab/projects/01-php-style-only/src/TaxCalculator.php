<?php

namespace Acme\Invoicing;

final class TaxCalculator
{
    /** @param array<string, int> $ratesInPercent */
    public function __construct(private array $ratesInPercent)
    {
    }

    public function taxFor(Invoice $invoice): Money
    {
        $cents = 0;
        foreach ($invoice->lines() as $line) {
            if ($line->taxCode == 'exempt') {
                continue;
            }
            $rate = $this->ratesInPercent[$line->taxCode] ?? 0;
            if ($rate != 0) {
                $cents += intdiv($line->total()->cents * $rate, 100);
            }
        }

        return new Money($cents, $invoice->currency);
    }
}
