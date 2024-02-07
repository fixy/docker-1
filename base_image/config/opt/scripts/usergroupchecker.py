#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Check user and group file and create users and groups as needed"""

import sys
import os.path
import pwd
import grp
import datetime
import subprocess
import yaml

# Content of usergroup file under /etc/usergroups/user-group
#groups:
#  gpuusers:
#    name: 'gpuusers'
#    gid: 4444
#  uerj:
#    name: 'uerj'
#    gid: 4999
#  docker:
#    name: 'docker'
#    gid: 5555
#  allcit:
#    name: 'allcit'
#    gid: 6666
#  sdntestbed:
#    name: 'sdntestbed'
#    gid: 7777
#  qnet:
#    name: 'qnet'
#    gid: 8888
#  btl:
#    name: 'btl'
#    gid: 9999
#users:
#  jbalcas:
#    username: jbalcas
#    full_name: Justas Balcas
#    email: jbalcas@caltech.edu
#    id: 3000
#    expiry: '2024-07-01'
#    dn:
#      - '/DC=ch/DC=cern/OU=Organic Units/OU=Users/CN=jbalcas/CN=751133/CN=Justas Balcas'
#    groups:
#      - allcit
#      - cms
#      - gpuusers
#      - sdntestbed

# Load file and check that users and groups are defined
# if not, create user and add user to group
# Also create grid-mapfile and voms-mapfile and add all users/groups as needed
def runCmd(command):
    """Run command and print output"""
    process = subprocess.Popen(command,stdout=subprocess.PIPE, shell=True)
    stdout, stderr = process.communicate()
    exitCode = process.wait()
    if stdout:
        for line in stdout.splitlines():
            print(line.decode('utf-8'))
    if stderr:
        for line in stderr.splitlines():
            print(line.decode('utf-8'))
    if exitCode != 0:
        print(f"Error while executing command: {command}")
        sys.exit(1)

def groupCheck(group, vals):
    """Check if group exists, if not, create it"""
    if 'name' not in vals or 'gid' not in vals:
        print(f'WARNING! Group name ir GID not defined. {group}')
        return
    if group != vals['name']:
        print(f'WARNING! Group name does not match. {group} != {vals["name"]}')
        return
    try:
        grp.getgrnam(group)
    except KeyError:
        print(f"Creating group: {vals['name']}")
        # groupadd -g 3000 jbalcas
        runCmd(f"groupadd -f -g {vals['gid']} {vals['name']}")

def createUser(username, uid, groups):
    """Create user and add to groups"""
    try:
        pwd.getpwnam(username)
    except KeyError:
        print(f"User does not exist. Creating user: {username}")
        grLine = ",".join(groups)
        if grLine:
            runCmd(f"useradd -u {uid} -s /sbin/nologin -M -G {grLine} {username}")
        else:
            runCmd(f"useradd -u {uid} -s /sbin/nologin -M {username}")
        return
    # If user exists, then check if groups are correct
    groups = [g.gr_name for g in grp.getgrall() if username in g.gr_mem]
    gid = pwd.getpwnam(username).pw_gid
    groups.append(grp.getgrgid(gid).gr_name)
    if set(groups) != set(groups):
        print(f"Groups are not correct. Fixing groups for user: {username}")
        grLine = ",".join(groups)
        runCmd(f"usermod -G {grLine} {username}")

def deleteUser(username):
    """Delete user"""
    try:
        pwd.getpwnam(username)
    except KeyError:
        print(f"User does not exist. Nothing to delete: {username}")
        return
    print(f"Deleting user: {username}")
    runCmd(f"userdel {username}")

def userCheck(username, vals):
    """Check if user exists, if not, create it"""
    action = 'create'
    # If username or id is not defined, then skip
    if 'username' not in vals or 'id' not in vals:
        print(f'WARNING! Username ir ID not defined. {vals}')
        return
    # If username does not match, then skip
    if username != vals['username']:
        print(f'WARNING! Username does not match. {username} != {vals["username"]}')
        return
    # If it has a flag ensure: absent, then remove user
    if 'ensure' in vals and vals['ensure'] == 'absent':
        action = 'remove'
    # If expiry date is in the past, then remove user
    if 'expiry' in vals:
        activeDate = datetime.datetime.strptime(vals['expiry'], '%Y-%m-%d')
        if activeDate < datetime.datetime.now():
            action = 'remove'
    if action == 'remove':
        deleteUser(vals['username'])
    if action == 'create':
        createUser(vals['username'], vals['id'], vals['groups'])

def run():
    """Main run"""
    if not os.path.isfile("/etc/usergroups/user-group"):
        print("File /etc/usergroups/user-group not found")
        return
    with open("/etc/usergroups/user-group", "r", encoding='utf-8') as fd:
        data = yaml.load(fd)
    if "groups" in data:
        for key, vals in data["groups"].items():
            groupCheck(key, vals)
    if "users" in data:
        for key, vals in data["users"].items():
            userCheck(key, vals)

if __name__ == "__main__":
    run()
