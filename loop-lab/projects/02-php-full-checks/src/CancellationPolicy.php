<?php

declare(strict_types=1);

namespace Acme\Bookings;

use DateInterval;
use DateTimeImmutable;

final class CancellationPolicy
{
    private const FREE_CANCELLATION_HOURS = 48;
    private const LATE_FEE_PERCENT = 50;

    /**
     * Fee in cents for cancelling at $now.
     *
     * Free up to and including exactly 48 hours before check-in, half the
     * price after that, the full price once check-in time has been reached.
     */
    public function feeCents(Booking $booking, DateTimeImmutable $now): int
    {
        $price = $booking->nights() * $booking->nightlyRateCents;

        if ($now >= $booking->checkIn()) {
            return $price;
        }

        $freeUntil = $booking->checkIn()->sub(new DateInterval('PT' . self::FREE_CANCELLATION_HOURS . 'H'));
        if ($now <= $freeUntil) {
            return 0;
        }

        return intdiv($price * self::LATE_FEE_PERCENT, 100);
    }
}
