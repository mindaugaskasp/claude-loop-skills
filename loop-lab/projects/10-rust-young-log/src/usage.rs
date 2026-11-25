use std::collections::BTreeMap;

use crate::error::Error;
use crate::reading::Reading;

/// Water used by one plot between its first and its last reading.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Usage {
    pub plot: String,
    pub litres: u64,
}

/// Groups the readings by plot and takes last minus first. Plots come out in name order.
pub fn usage_per_plot(readings: &[Reading]) -> Result<Vec<Usage>, Error> {
    let mut by_plot: BTreeMap<&str, Vec<&Reading>> = BTreeMap::new();
    for reading in readings {
        by_plot
            .entry(reading.plot.as_str())
            .or_default()
            .push(reading);
    }

    let mut result = Vec::new();
    for (plot, mut list) in by_plot {
        list.sort_by(|a, b| a.date.cmp(&b.date));
        let first = list.first().unwrap();
        let last = list.last().unwrap();
        if last.litres < first.litres {
            return Err(Error::MeterWentBackwards {
                plot: plot.to_string(),
            });
        }
        result.push(Usage {
            plot: plot.to_string(),
            litres: last.litres - first.litres,
        });
    }
    Ok(result)
}
