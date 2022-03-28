#!/bin/sh

sed -i 's/\t/    /g' "${1}"

if [ -z "$1" ]; then
	echo "Usage: lint.sh FILE_NAME"
else
	echo "\nAutopep magic...\n"
	autopep8 --in-place "${1}" || exit 1
	echo "\nPylint checking...\n"
	pylint -d W0311,W0703,W1505,C0301,R0913 "${1}" || exit 1
	echo "\nPycodestyle checking...\n"
	pycodestyle "${1}" || exit 1
fi
