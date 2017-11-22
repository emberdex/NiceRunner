# NiceRunner
An easy way to run multiple iterations of the same code.

## Instructions

- This script requires python3 to run.
- Only tested on a Linux machine, but **should** work on Windows. Open an issue if not!

Simply execute `./nicerunner.py <file to run>`.

## Command-line arguments

- `-n <number> || --number-iterations <number>` defines the number of iterations to run.
- `-t <seconds> || --time-limit <seconds>` determines the time to wait before considering the process deadlocked and killing it.

For example, `./nicerunner -n 100 -t 5 ./program` runs `./program` 100 times, and waits for 5 seconds before killing the process.
