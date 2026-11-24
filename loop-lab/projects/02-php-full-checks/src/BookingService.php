<?php

declare(strict_types=1);

namespace Acme\Bookings;

use DateTimeImmutable;

final class BookingService
{
    public function __construct(
        private BookingRepository $bookings,
    ) {
    }

    public function cancel(int $bookingId): void
    {
        $booking = $this->bookings->find($bookingId);
        $booking->cancel();
        $this->bookings->save($booking);
    }

    public function reschedule(int $bookingId, DateTimeImmutable $checkIn, DateTimeImmutable $checkOut): void
    {
        $booking = $this->bookings->find($bookingId);
        $booking->reschedule($checkIn, $checkOut);
        $this->bookings->save($booking);
    }

    public function isRoomFree(int $roomId, DateTimeImmutable $checkIn, DateTimeImmutable $checkOut): bool
    {
        foreach ($this->bookings->forRoom($roomId) as $booking) {
            if ($booking->isCancelled()) {
                continue;
            }
            if ($checkIn < $booking->checkOut() && $checkOut > $booking->checkIn()) {
                return false;
            }
        }

        return true;
    }
}
