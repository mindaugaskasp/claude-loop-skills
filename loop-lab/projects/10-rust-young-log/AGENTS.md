# Notes for coding agents

- Run `make check` before you say a task is done. It runs the formatter check, clippy and the tests.
- Water is counted in whole litres (`u64`) and money in whole cents (`u64`). Convert to cubic metres or euros only when printing.
- No crates from outside. The standard library is enough for this tool.
- Every error a member of the committee could see goes through `plotwatch::Error` and says which line of the file is wrong.
- One pull request per change, on Codeberg. Aiste and Jonas review each other's pull requests.
