#! /usr/bin/env python3
# -*- coding: utf-8 -*-

sn_file = "/tmp/sn_file.txt"

def write_sn_file(sn):
    sn = str(sn)
    with open(sn_file, 'w') as f:
        f.write(sn)
        f.truncate()


def read_sn_file():
    with open(sn_file) as f:
        sn = f.read().replace('\n', '')
    sn = str(sn)
    return sn


def increment_sn(sn):
    sn = int(sn)
    sn = sn + 1
    sn = str(sn)
    sn = sn.rjust(4, '0')
    return sn


sn = 0
sn = write_sn_file(sn)

for i in range(1, 10000):
    sn = read_sn_file()
    sn = increment_sn(sn)
    write_sn_file(sn)
    sn = read_sn_file()
    print(sn)

