<?php

declare(strict_types=1);

namespace Acme\Bookings\Tests;

use Acme\Bookings\Booking;
use Acme\Bookings\PriceCalculator;
use DateTimeImmutable;
use PHPUnit\Framework\TestCase;

final class PriceCalculatorTest extends TestCase
{
    public function testWeekdayNightsHaveNoSurcharge(): void
    {
        // Monday to Thursday: three weekday nights.
        $booking = new Booking(1, 7, 'guest@example.com', new DateTimeImmutable('2026-03-02 15:00'), new DateTimeImmutable('2026-03-05 15:00'), 9000);

        self::assertSame(27000, (new PriceCalculator())->totalCents($booking));
    }

    public function testFridayAndSaturdayNightsCostFifteenPercentMore(): void
    {
        // Friday to Sunday: two weekend nights.
        $booking = new Booking(1, 7, 'guest@example.com', new DateTimeImmutable('2026-03-06 15:00'), new DateTimeImmutable('2026-03-08 15:00'), 9000);

        self::assertSame(20700, (new PriceCalculator())->totalCents($booking));
    }
}
