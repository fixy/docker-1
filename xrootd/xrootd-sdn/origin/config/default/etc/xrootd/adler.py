#!/usr/bin/env python3
import sys

filename = sys.argv[1]

allfiles = {}
with open('/etc/xrootd/allfiles.txt', 'r') as fd:
    alllines = fd.read().split('\n')
    for item in alllines:
        if not item:
            continue
        item = item.split(' ')
        allfiles[item[1][1:]] = item[0]

if filename in allfiles:
    sys.stdout.write(str(allfiles[filename]) + '\n')
else:
    sys.stdout.write('12345678 \n')

