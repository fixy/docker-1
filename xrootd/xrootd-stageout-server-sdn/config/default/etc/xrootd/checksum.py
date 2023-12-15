#!/usr/bin/env python3
#
#   Computes the Adler32 checksum of input path.
#
#   Saul Youssef, 2021
#

import sys,os,time
import pwd,socket

BLOCKSIZE=2*1024*1024
from zlib import adler32

def checksum(path):
    val = 1
    with open(path, 'rb')  as fd:
        while True:
            data = fd.read(BLOCKSIZE)
            if not data: break
            val = adler32(data,val)
    if val<0: val += 2**32
    return hex(val)[2:10].zfill(8).lower()

class log(object):
    def __init__(self):
        self._dir = os.path.dirname(os.path.abspath(__file__))
    def write(self,entries):
        t = time.localtime()
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S',t)
        day       = time.strftime('%Y-%m-%d'         ,t)
        try    : user = pwd.getpwuid(os.getuid())[0]
        except : user = 'unknown'
        try    : host = socket.gethostname()
        except : host = 'unknown'
        LOGPATH = os.path.join(self._dir,'adler_'+day+'.log')
        Entries = [['time',timestamp],['user',user],['host',host]]+[[entry[0],entry[1].replace('=',':').replace(',',' ')] for entry in entries]
        logline = ', '.join(['='.join(entry) for entry in Entries])
        os.system('echo "'+logline+'" >> '+LOGPATH)
        return self

logFile = log()
stubName = '/storage/cms/'

if len(sys.argv)<2:
    logFile.write(['error','No input absolute path provided'])
    sys.stderr.write('No input absolute path provided')
    sys.exit(1)


inpName = os.path.realpath(sys.argv[1])
if inpName.startswith(stubName):
    fileName = (inpName.split(stubName))[1]
else:
    fileName = inpName
fullName = stubName + fileName
altName = '/rucio/cksums' + fileName

if not os.path.exists(fullName):
    msg = 'Input file does not exist'
    logFile.write([['error',msg],['path',fullName]])
    sys.stderr.write(msg+'\n')
    sys.exit(1)
elif not os.path.isfile(fullName):
    msg = 'Input is not a regular file'
    logFile.write([['error',msg],['path',fullName]])
    sys.stderr.write(msg+'\n')
elif 'cksums' in fullName:
    msg = 'Input file is a checksum file'
    logFile.write([['error',msg],['fullName',path]])
    sys.stderr.write(msg)
    sys.exit(1)
#
#    Read checksum from cached value, if available, otherwise, compute
#
try:
    if os.path.exists(altName):  # read cached checksum
        f = open(altName,'r')
        adler = f.read()
        f.close()
        bytes = os.path.getsize(altName)
        entries = [['action','Get cached checksum'],['path',inpName],['adler',adler],['bytes',str(bytes)]]
        logFile.write(entries)
        sys.stdout.write(str(adler) + '\n')
        sys.exit(0)
    else:                              # compute adler checksum from file contents
        ts = time.time()
        adler = checksum(fullName)
        te = time.time()
        bytes = os.path.getsize(fullName)
        mbytes = float(bytes)/1000000.0
        dt = max(0.001,te-ts)
        rate = mbytes/dt


        if not os.path.exists(os.path.dirname(altName)):
            try:
                os.makedirs(os.path.dirname(altName))
            except OSError as exc: # Guard against race condition
                pass

        f = open(altName,'w')  # save special file atomically
        f.write(adler)
        f.close()

        entries = [['action','Compute checksum'],['path',inpName],['adler',adler],['bytes',str(bytes)],['duration',str(dt)],['rate',str(rate)]]
        logFile.write(entries)
        sys.stdout.write(str(adler) + '\n')
        sys.exit(0)
except Exception as e:
    entries = [['error',str(e)],['path',inpName]]
    logFile.write(entries)
    sys.stderr.write(str(e))
    sys.exit(1)
