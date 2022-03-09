#!/usr/bin/python3
import os
import socket
import json
import yaml
import subprocess
import psutil

compFile = 'docker-compose.yml'
compContent = {}

with open(compFile, 'r') as fd:
    compContent = yaml.safe_load(fd)
print(compContent)

newVolumes = []
volumes = []
for item in compContent['services']['xcache-server']['volumes']:
    if not item.startswith('/data'):
        newVolumes.append(item)


process = subprocess.run("lsblk --json -o NAME,MOUNTPOINT".split(), stdout=subprocess.PIPE)
blockdevices = json.loads(process.stdout)
for item in blockdevices.get('blockdevices', []):
    for chitem in item.get('children', []):
        if chitem['mountpoint'] and chitem['mountpoint'].startswith('/data'):
           newVolumes.append("%s:%s:rw" % (chitem['mountpoint'], chitem['mountpoint']))
           volumes.append('oss.space data %s/xcache' % chitem['mountpoint'])

compContent['services']['xcache-server']['volumes'] = newVolumes
with open(compFile, 'w') as fd:
    yaml.dump(compContent, fd)

xdir = './config/%s/etc/xrootd/config.d' % socket.gethostname().split('.', 1)[0]
try:
    os.mkdir(xdir)
except FileExistsError:
    pass
with open('%s/90-custom.cfg' % xdir, 'w') as fd:
    fd.write('='*40 + '\n')
    fd.write('AUTO DISKS CONFIGURED BY SCRIPT\n')
    fd.write('='*40 + '\n\n')
    for item in volumes:
        fd.write(item + '\n')
    fd.write('\n\n')
    fd.write('='*40 + '\n')
    fd.write('AUTO MEMORY FOR XROOTD. 70% of all available mem\n')
    fd.write('='*40 + '\n\n')
    totalMem = int(psutil.virtual_memory().total * 0.7/1024/1024/1204)
    fd.write('pfc.ram %sg' % totalMem)
