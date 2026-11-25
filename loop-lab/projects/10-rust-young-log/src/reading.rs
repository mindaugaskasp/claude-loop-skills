use crate::error::Error;

/// One meter reading: the meter of `plot` showed `litres` on `date`.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Reading {
    pub plot: String,
    /// ISO date, for example 2026-04-12. Kept as text; it sorts correctly.
    pub date: String,
    pub litres: u64,
}

/// Reads the CSV text with the header `plot,date,litres`.
pub fn parse_readings(text: &str) -> Result<Vec<Reading>, Error> {
    let mut readings = Vec::new();
    for (index, line) in text.lines().enumerate().skip(1) {
        if line.trim().is_empty() {
            continue;
        }
        let line_number = index + 1;
        let fields: Vec<&str> = line.split(',').map(str::trim).collect();
        if fields.len() != 3 {
            return Err(Error::BadLine {
                line: line_number,
                reason: format!("expected 3 columns, found {}", fields.len()),
            });
        }
        if !looks_like_date(fields[1]) {
            return Err(Error::BadLine {
                line: line_number,
                reason: format!("'{}' is not a date like 2026-04-12", fields[1]),
            });
        }
        let litres = fields[2].parse::<u64>().map_err(|_| Error::BadLine {
            line: line_number,
            reason: format!("'{}' is not a whole number of litres", fields[2]),
        })?;
        readings.push(Reading {
            plot: fields[0].to_string(),
            date: fields[1].to_string(),
            litres,
        });
    }
    Ok(readings)
}

fn looks_like_date(text: &str) -> bool {
    let bytes = text.as_bytes();
    bytes.len() == 10
        && bytes[4] == b'-'
        && bytes[7] == b'-'
        && bytes
            .iter()
            .enumerate()
            .all(|(i, b)| i == 4 || i == 7 || b.is_ascii_digit())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn reads_two_lines() {
        let readings = parse_readings("plot,date,litres\nA1,2026-04-12,10\nA1,2026-10-18,25\n");
        assert_eq!(readings.map(|r| r.len()), Ok(2));
    }

    #[test]
    fn names_the_line_that_is_wrong() {
        let result = parse_readings("plot,date,litres\nA1,2026-04-12,10\nA2,2026-04-12,ten\n");
        assert!(matches!(result, Err(Error::BadLine { line: 3, .. })));
    }

    #[test]
    fn rejects_a_date_in_another_order() {
        let result = parse_readings("plot,date,litres\nA1,12.04.2026,10\n");
        assert!(matches!(result, Err(Error::BadLine { line: 2, .. })));
    }
}
