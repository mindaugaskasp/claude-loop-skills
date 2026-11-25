use std::env;
use std::fs;
use std::process::ExitCode;

use plotwatch::bill::{bill_cents, format_cents, tariff_from_arg};
use plotwatch::reading::parse_readings;
use plotwatch::usage::usage_per_plot;
use plotwatch::Error;

fn run(path: &str, price: &str) -> Result<(), Error> {
    let text = fs::read_to_string(path).map_err(|e| Error::Io(format!("{path}: {e}")))?;
    let readings = parse_readings(&text)?;
    let tariff = tariff_from_arg(price);

    println!("{:<6} {:>10} {:>14}", "plot", "litres", "to pay");
    let mut total = 0;
    for usage in usage_per_plot(&readings)? {
        let cents = bill_cents(&usage, &tariff);
        total += cents;
        println!(
            "{:<6} {:>10} {:>14}",
            usage.plot,
            usage.litres,
            format_cents(cents)
        );
    }
    println!("{:<6} {:>10} {:>14}", "total", "", format_cents(total));
    Ok(())
}

fn main() -> ExitCode {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 || args.len() > 3 {
        eprintln!("usage: plotwatch <readings.csv> [cents per cubic metre]");
        return ExitCode::from(2);
    }
    let price = args.get(2).map_or("310", String::as_str);
    match run(&args[1], price) {
        Ok(()) => ExitCode::SUCCESS,
        Err(error) => {
            eprintln!("plotwatch: {error}");
            ExitCode::FAILURE
        }
    }
}
