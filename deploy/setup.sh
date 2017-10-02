#! /bin/bash
# setup.sh - Sets up necessary files and directories.

USER="pi"
APP="part-label"
APP_DIR="/home/${USER}/${APP}"


DATE_FILE="/tmp/date_file.txt"
SN_FILE="/tmp/sn_file.txt"
LOG_FILE="${APP_DIR}/log/serial_numbers.log"

echo
echo "Part Label Printer Setup Script"
echo
echo "Creating files..."

echo $DATE_FILE
echo "" > $DATE_FILE

echo $SN_FILE
echo 0000 > $SN_FILE

echo $LOG_FILE
mkdir -p log
touch $LOG_FILE

echo
echo "Done."
