#! /bin/bash
# setup.sh - Sets up necessary files and directories.

USER="pi"
APP="part-label"
APP_DIR="/home/${USER}/${APP}"

PRESS_ID_FILE="/boot/PRESS_ID"
DATE_FILE="${APP_DIR}/date_file.txt"
SN_FILE="${APP_DIR}sn_file.txt"
LOG_FILE="${APP_DIR}/log/serial_numbers.log"

echo
echo "Part Label Printer Setup Script"
echo
echo "Creating files..."
echo
echo "Assigning Press ID"
echo
echo "Please enter the Press ID"
read PRESS_ID
echo ${PRESS_ID} | sudo tee ${PRESS_ID_FILE} > /dev/null
echo

echo $DATE_FILE
echo "" > $DATE_FILE

echo $SN_FILE
echo 0000 > $SN_FILE

echo $LOG_FILE
mkdir -p log
touch $LOG_FILE

echo
echo "Done."
