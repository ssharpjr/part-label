#!/usr/bin/env bash
# start.sh - Start the application.

PYTHON_EXE="env/bin/python3"
APP="main.py"

# Start virtual env
. env/bin/activate

$PYTHON_EXE $APP
