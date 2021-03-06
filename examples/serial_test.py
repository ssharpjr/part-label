#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4
###############################################################################

import serial



# files = ['setup.zpl', 'data1.zpl', 'data2.zpl']
files = ['delete_image.zpl']

for file in files:
    ser = serial.Serial('/dev/ttyUSB0', baudrate=9600, bytesize=8, parity='N',
                        stopbits=1, xonxoff=0, timeout=5)
    with open(file, 'r') as f:
        label = f.read()
        ser.write(label.encode())
        ser.close()

