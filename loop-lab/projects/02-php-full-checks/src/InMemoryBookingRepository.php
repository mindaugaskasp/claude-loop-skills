<?php

declare(strict_types=1);

namespace Acme\Bookings;

final class InMemoryBookingRepository implements BookingRepository
{
    /** @var array<int, Booking> */
    private array $bookings = [];

    public function find(int $id): ?Booking
    {
        return $this->bookings[$id] ?? null;
    }

    public function save(Booking $booking): void
    {
        $this->bookings[$booking->id] = $booking;
    }

    public function forRoom(int $roomId): array
    {
        $result = [];
        foreach ($this->bookings as $booking) {
            if ($booking->roomId === $roomId) {
                $result[] = $booking;
            }
        }

        return $result;
    }
}
