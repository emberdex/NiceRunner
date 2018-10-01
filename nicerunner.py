#!/usr/bin/env python3

'''
NiceRunner - an easy way to run multiple iterations of the same code.
Developed by monotron (https://github.com/monotron)

'''

import argparse
import os
import sys
import time
import subprocess
import signal

class ANSI:
	reset = '\033[0m'
	yelw = '\033[93m'
	green = '\033[92m'
	red = '\033[91m'

class RunnerData:
	iterations = 10
	executable = ""
	time_limit = 0
	save_file = False

class CommandLineArguments:
	force_ansi = False

# Function to parse command line arguments.
def parse_arguments():
	# Set up the command line argument parser.
	argument_parser = argparse.ArgumentParser()

	# Add the arguments to the parser.
	argument_parser.add_argument("executable", help="The executable to run.")
	argument_parser.add_argument("-n", "--number-iterations", help="The number of iterations to run.")
	argument_parser.add_argument("-t", "--time-limit", help="The time to wait before considering the process to be locked, in seconds.")
	argument_parser.add_argument("-s", "--save-output", help="Save stdout and stderr to a file.", action="store_true")
	argument_parser.add_argument("-a", "--force-ansi", help="Force ANSI characters to be used on Windows.", action="store_true")

	# Read the passed-in arguments and parse them.
	args = argument_parser.parse_args()

	# Update the runner data based on the arguments.
	if args.number_iterations:
		try:
			RunnerData.iterations = int(args.number_iterations)
		except ValueError:
			print("Number of iterations must be an integer.")
			sys.exit(1)

	RunnerData.executable = args.executable

	if args.time_limit:
		try:
			RunnerData.time_limit = int(args.time_limit)
		except ValueError:
			print("Timeout value must be an integer.")
			sys.exit(1)

	if args.save_output:
		RunnerData.save_file = True

	if args.force_ansi:
		CommandLineArguments.force_ansi = True

def execute():
	# Check if the path exists.
	if not os.path.exists(RunnerData.executable):
		print("File \"{}\" not found.".format(RunnerData.executable))
		sys.exit(1)

	# Check if we're working with a file or a path.
	if not os.path.isfile(RunnerData.executable):
		print("Please pass in a file as the executable.")
		sys.exit(1)

	print("Going to execute file \"{}\" {} times.".format(RunnerData.executable, RunnerData.iterations))

	stderr_file = ""
	stdout_file = ""

	if RunnerData.save_file:
		stderr_filename = "{}.stderr.log".format(RunnerData.executable)
		stdout_filename = "{}.stdout.log".format(RunnerData.executable)

		stderr_file = open(stderr_filename, "w")
		stdout_file = open(stdout_filename, "w")

		print("Logging to {} and {}.".format(stdout_filename, stderr_filename))
		stdout_file.write("=* Running process {} {} times. *=".format(RunnerData.executable, RunnerData.iterations))

	for x in range(0, RunnerData.iterations):
		start = time.time()
		timed_out = False
		process = ""

		if RunnerData.save_file:
			if hasattr(os, 'setsid'):
				process = subprocess.Popen(RunnerData.executable, stdout=stdout_file, stderr=stderr_file, preexec_fn=os.setsid)
			else:
				process = subprocess.Popen(RunnerData.executable, stdout=stdout_file, stderr=stderr_file)
		else:
			if hasattr(os, 'setsid'):
				process = subprocess.Popen(RunnerData.executable, stdout=subprocess.PIPE, stderr=subprocess.PIPE, preexec_fn=os.setsid)
			else:
				process = subprocess.Popen(RunnerData.executable, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		
		while process.poll() == None:
			if RunnerData.time_limit > 0 and (time.time() - start) > RunnerData.time_limit:
				if hasattr(os, 'killpg') and hasattr(os, 'getpgid') and hasattr(signal, 'signal.SIGKILL'):
					os.killpg(os.getpgid(process.pid), signal.SIGKILL)
				else:
					try:
						os.kill(process.pid, signal.SIGTERM)
					except PermissionError:
						print("{}Failed to kill process.\nPlease run this script as an administrator.{}".format(ANSI.red, ANSI.reset))
				timed_out = True

				if RunnerData.save_file is True: 
					stderr_file.write("=* Iteration {} timed out and was killed after {} seconds. *=".format(x, RunnerData.time_limit))

				continue

		end = time.time()
		timeval = round(end - start, 3)

		if timed_out: 
			print("{}Iteration {} timed out.{}".format(ANSI.red, x, ANSI.reset))
		else:
			print("{}Iteration {} took {} seconds.{}".format(ANSI.green, x, timeval, ANSI.reset), end="")
			print("{} (return value: {}){}".format(ANSI.yelw, process.returncode, ANSI.reset), end="")
			print("")

	if RunnerData.save_file:
		stderr_file.flush()
		stdout_file.flush()

		stdout_file.close()
		stderr_file.close()

parse_arguments()

# Remove ANSI values for Windows, as the Windows command prompt does not support these.
if os.name is "nt" and CommandLineArguments.force_ansi is not True:
	ANSI.reset = ""
	ANSI.yelw = ""
	ANSI.red = ""
	ANSI.green = ""

	print("ANSI formatting is not supported on Windows and has been disabled.")

if __name__ == "__main__":
	execute()
