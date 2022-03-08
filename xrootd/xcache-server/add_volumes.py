#!/usr/bin/python3
import json
import yaml
import subprocess

compFile = 'docker-compose.yml'
compContent = {}

with open(compFile, 'r') as fd:
    compContent = yaml.safe_load(fd)
print(compContent)

newVolumes = []
for item in compContent['services']['xcache-server']['volumes']:
    if not item.startswith('/data'):
        newVolumes.append(item)


process = subprocess.run("lsblk --json -o NAME,MOUNTPOINT".split(), stdout=subprocess.PIPE)
blockdevices = json.loads(process.stdout)
for item in blockdevices.get('blockdevices', []):
    for chitem in item.get('children', []):
        if chitem['mountpoint'] and chitem['mountpoint'].startswith('/data'):
           newVolumes.append("%s:%s:rw" % (chitem['mountpoint'], chitem['mountpoint']))

compContent['services']['xcache-server']['volumes'] = newVolumes
with open(compFile, 'w') as fd:
    yaml.dump(compContent, fd)

