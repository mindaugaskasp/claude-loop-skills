use std::fmt;

/// Everything that can go wrong in a way the committee should read about.
#[derive(Debug, PartialEq, Eq)]
pub enum Error {
    /// A line of the readings file could not be understood.
    BadLine { line: usize, reason: String },
    /// The last reading of a plot is lower than its first one.
    MeterWentBackwards { plot: String },
    /// The file could not be read at all.
    Io(String),
}

impl fmt::Display for Error {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Error::BadLine { line, reason } => write!(f, "line {line}: {reason}"),
            Error::MeterWentBackwards { plot } => {
                write!(
                    f,
                    "plot {plot}: the last reading is lower than the first one"
                )
            }
            Error::Io(reason) => write!(f, "cannot read the file: {reason}"),
        }
    }
}

impl std::error::Error for Error {}
