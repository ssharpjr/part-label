#!/usr/bin/env bash
# start.sh - Start the application.

PYTHON_EXE="/usr/bin/python3"
APP="print_label.py"

# Start virtual env
. env/bin/activate

$PYTHON_EXE $APP
