use crate::usage::Usage;

/// Prices, in whole cents.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct Tariff {
    pub cents_per_cubic_metre: u64,
    pub standing_charge_cents: u64,
}

/// The fixed yearly charge every plot pays, in cents.
pub const STANDING_CHARGE_CENTS: u64 = 1200;

/// Builds the tariff from the price typed on the command line.
pub fn tariff_from_arg(arg: &str) -> Tariff {
    Tariff {
        cents_per_cubic_metre: arg.trim().parse().unwrap(),
        standing_charge_cents: STANDING_CHARGE_CENTS,
    }
}

/// What a plot owes, in cents. The water part is rounded to the nearest cent, half up.
pub fn bill_cents(usage: &Usage, tariff: &Tariff) -> u64 {
    let water = (usage.litres * tariff.cents_per_cubic_metre + 500) / 1000;
    water + tariff.standing_charge_cents
}

/// 12345 becomes "123.45 EUR".
pub fn format_cents(cents: u64) -> String {
    format!("{}.{:02} EUR", cents / 100, cents % 100)
}

#[cfg(test)]
mod tests {
    use super::*;

    fn usage(litres: u64) -> Usage {
        Usage {
            plot: "A1".to_string(),
            litres,
        }
    }

    #[test]
    fn a_plot_that_used_nothing_pays_the_standing_charge() {
        let tariff = tariff_from_arg("310");
        assert_eq!(bill_cents(&usage(0), &tariff), 1200);
    }

    #[test]
    fn water_is_rounded_to_the_nearest_cent() {
        let tariff = Tariff {
            cents_per_cubic_metre: 310,
            standing_charge_cents: 0,
        };
        // 27 750 litres at 3.10 EUR per cubic metre is 86.025 EUR.
        assert_eq!(bill_cents(&usage(27_750), &tariff), 8603);
    }

    #[test]
    fn cents_are_printed_with_two_digits() {
        assert_eq!(format_cents(1205), "12.05 EUR");
    }
}
