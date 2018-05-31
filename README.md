# NiceRunner
An easy way to run multiple iterations of the same code.
![A screenshot of NiceRunner in action.](https://i.imgur.com/JgkyzIW.png "A screenshot of NiceRunner in action.")

## Instructions

- This script requires python3 to run.
- Tested on Windows and Linux, but should work on macOS. If not, feel free to open an issue!

Simply execute `./nicerunner.py <file to run>`.

If you want to add NiceRunner to /usr/bin, run the following commands as root:
- `chmod +x install.sh`
- `./install.sh`

## Command-line arguments

- `-n <number> || --number-iterations <number>` defines the number of iterations to run.
- `-t <seconds> || --time-limit <seconds>` determines the time to wait before considering the process deadlocked and killing it.
- `-s || --save-file` saves stdout and stderr to a file in the same directory as the 
executable.

For example, `./nicerunner -n 100 -t 5 ./program` runs `./program` 100 times, and waits for 5 seconds before killing the process.
