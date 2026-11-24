<?php

declare(strict_types=1);

namespace Acme\Bookings;

use DateTimeImmutable;
use InvalidArgumentException;

final class Booking
{
    private bool $cancelled = false;

    public function __construct(
        public readonly int $id,
        public readonly int $roomId,
        public readonly string $guestEmail,
        private DateTimeImmutable $checkIn,
        private DateTimeImmutable $checkOut,
        public readonly int $nightlyRateCents,
    ) {
        self::assertValidStay($checkIn, $checkOut);
    }

    public function checkIn(): DateTimeImmutable
    {
        return $this->checkIn;
    }

    public function checkOut(): DateTimeImmutable
    {
        return $this->checkOut;
    }

    public function nights(): int
    {
        return (int) $this->checkIn->diff($this->checkOut)->days;
    }

    public function reschedule(DateTimeImmutable $checkIn, DateTimeImmutable $checkOut): void
    {
        self::assertValidStay($checkIn, $checkOut);
        $this->checkIn = $checkIn;
        $this->checkOut = $checkOut;
    }

    public function cancel(): void
    {
        $this->cancelled = true;
    }

    public function isCancelled(): bool
    {
        return $this->cancelled;
    }

    private static function assertValidStay(DateTimeImmutable $checkIn, DateTimeImmutable $checkOut): void
    {
        if ($checkOut <= $checkIn) {
            throw new InvalidArgumentException('Check-out must be after check-in.');
        }
    }
}
