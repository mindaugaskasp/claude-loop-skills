<?php

namespace Acme\Invoicing\Http;

use Acme\Invoicing\InvoiceRepository;
use Acme\Invoicing\TaxCalculator;

final class InvoiceController
{
    public function __construct(
        private InvoiceRepository $invoices,
        private TaxCalculator $tax,
    ) {
    }

    /** @return array<string, mixed> */
    public function show(string $number): array
    {
        $invoice = $this->invoices->find($number);
        if ($invoice === null) {
            return ['status' => 404, 'error' => 'Invoice not found'];
        }

        $subtotal = $invoice->subtotal();
        $tax = $this->tax->taxFor($invoice);

        return [
            'status' => 200,
            'number' => $invoice->number,
            'subtotal' => $subtotal->format(),
            'tax' => $tax->format(),
            'total' => $subtotal->add($tax)->format(),
        ];
    }
}
