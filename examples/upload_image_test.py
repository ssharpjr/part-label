#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4
###############################################################################

import serial


files = ['IMAGE1.GRF',
         'IMAGE2.GRF',
         'IMAGE3.GRF',
         'IMAGE4.GRF',
         'IMAGE5.GRF',
         'IMAGE6.GRF']


for file in files:
    ser = serial.Serial('/dev/ttyUSB0', baudrate=9600, bytesize=8, parity='N',
                        stopbits=1, xonxoff=0, timeout=5)
    with open(file, 'r') as f:
        label = f.read()
        ser.write(label.encode())
        ser.close()

