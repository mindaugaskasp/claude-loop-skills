<?php

declare(strict_types=1);

namespace Acme\Bookings\Tests;

use Acme\Bookings\Booking;
use DateTimeImmutable;
use InvalidArgumentException;
use PHPUnit\Framework\TestCase;

final class BookingTest extends TestCase
{
    public function testCountsNights(): void
    {
        $booking = new Booking(1, 7, 'guest@example.com', new DateTimeImmutable('2026-03-02 15:00'), new DateTimeImmutable('2026-03-05 15:00'), 9000);

        self::assertSame(3, $booking->nights());
    }

    public function testRejectsCheckOutBeforeCheckIn(): void
    {
        $this->expectException(InvalidArgumentException::class);

        new Booking(1, 7, 'guest@example.com', new DateTimeImmutable('2026-03-05 15:00'), new DateTimeImmutable('2026-03-02 15:00'), 9000);
    }

    public function testCancel(): void
    {
        $booking = new Booking(1, 7, 'guest@example.com', new DateTimeImmutable('2026-03-02 15:00'), new DateTimeImmutable('2026-03-05 15:00'), 9000);
        $booking->cancel();

        self::assertTrue($booking->isCancelled());
    }
}
