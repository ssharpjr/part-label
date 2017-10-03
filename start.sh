#!/usr/bin/env bash
# start.sh - Start the application.

APP="print_label.py"

# Start virtual env
source env/bin/activate

python3 $APP
