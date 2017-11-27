#!/bin/bash

# Are we root?
if [[ $EUID -ne 0 ]]; then
	# Check if sudo is installed on this system.
	which sudo > /dev/null

	if [[ $? -ne 0 ]]; then
		echo "Please run this script as root."
		exit 1;
	else
		sudo $0
		exit $?;
	fi
fi

echo "Installing NiceRunner..."
cp "nicerunner.py" "/usr/bin/nicerunner"
chmod +x "/usr/bin/nicerunner"

exit 0