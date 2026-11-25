use plotwatch::reading::parse_readings;
use plotwatch::usage::usage_per_plot;
use plotwatch::Error;

const SPRING_AND_AUTUMN: &str = "plot,date,litres
A1,2026-04-12,104200
B4,2026-04-12,5120
A1,2026-10-18,131950
B4,2026-10-18,5120
";

#[test]
fn usage_is_last_reading_minus_first() {
    let readings = parse_readings(SPRING_AND_AUTUMN).expect("the sample parses");
    let usage = usage_per_plot(&readings).expect("the meters only go up");
    let litres: Vec<(&str, u64)> = usage.iter().map(|u| (u.plot.as_str(), u.litres)).collect();
    assert_eq!(litres, vec![("A1", 27_750), ("B4", 0)]);
}

#[test]
fn the_order_of_lines_in_the_file_does_not_matter() {
    let text = "plot,date,litres\nA1,2026-10-18,300\nA1,2026-04-12,100\n";
    let readings = parse_readings(text).expect("the sample parses");
    let usage = usage_per_plot(&readings).expect("the meters only go up");
    assert_eq!(usage[0].litres, 200);
}

#[test]
fn a_meter_that_went_backwards_is_an_error() {
    let text = "plot,date,litres\nA1,2026-04-12,300\nA1,2026-10-18,100\n";
    let readings = parse_readings(text).expect("the sample parses");
    assert_eq!(
        usage_per_plot(&readings),
        Err(Error::MeterWentBackwards {
            plot: "A1".to_string()
        })
    );
}
