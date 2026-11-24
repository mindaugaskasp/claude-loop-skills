<?php

declare(strict_types=1);

namespace Acme\Bookings;

interface BookingRepository
{
    public function find(int $id): ?Booking;

    public function save(Booking $booking): void;

    /** @return list<Booking> */
    public function forRoom(int $roomId): array;
}
