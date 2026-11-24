<?php

declare(strict_types=1);

namespace Acme\Invoicing;

final class InvoiceRepository
{
    /** @var array<string, Invoice> */
    private array $invoices = [];

    public function save(Invoice $invoice): void
    {
        $this->invoices[$invoice->number] = $invoice;
    }

    public function find(string $number): ?Invoice
    {
        foreach ($this->invoices as $invoice) {
            if ($invoice->number == $number) {
                return $invoice;
            }
        }

        return null;
    }

    /** @return Invoice[] */
    public function forCustomer(string $customerId): array
    {
        $found = [];
        foreach ($this->invoices as $invoice) {
            if ($invoice->customerId == $customerId) {
                $found[] = $invoice;
            }
        }

        return $found;
    }
}
