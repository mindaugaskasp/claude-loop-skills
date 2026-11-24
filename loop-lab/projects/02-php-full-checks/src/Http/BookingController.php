<?php

declare(strict_types=1);

namespace Acme\Bookings\Http;

use Acme\Bookings\BookingRepository;
use Acme\Bookings\PriceCalculator;

final class BookingController
{
    public function __construct(
        private BookingRepository $bookings,
        private PriceCalculator $prices,
    ) {
    }

    /** @return array<string, int|string|bool> */
    public function show(int $id): array
    {
        $booking = $this->bookings->find($id);

        return [
            'id' => $booking->id,
            'room' => $booking->roomId,
            'guest' => $booking->guestEmail,
            'check_in' => $booking->checkIn()->format('Y-m-d'),
            'check_out' => $booking->checkOut()->format('Y-m-d'),
            'cancelled' => $booking->isCancelled(),
            'total_cents' => $this->prices->totalCents($booking),
        ];
    }
}
