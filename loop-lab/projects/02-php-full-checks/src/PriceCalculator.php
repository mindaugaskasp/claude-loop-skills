<?php

declare(strict_types=1);

namespace Acme\Bookings;

use DateInterval;

final class PriceCalculator
{
    private const WEEKEND_SURCHARGE_PERCENT = 15;

    /** Total price of the stay in cents. Friday and Saturday nights cost 15 percent more. */
    public function totalCents(Booking $booking): int
    {
        $total = 0;
        $night = $booking->checkIn();
        for ($i = 0; $i < $booking->nights(); $i++) {
            $total += $booking->nightlyRateCents;
            if (in_array($night->format('N'), ['5', '6'], true)) {
                $total += intdiv($booking->nightlyRateCents * self::WEEKEND_SURCHARGE_PERCENT + 50, 100);
            }
            $night = $night->add(new DateInterval('P1D'));
        }

        return $total;
    }
}
