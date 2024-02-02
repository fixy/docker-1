#!/usr/bin/env python3
"""XRootD Log Monitoring Worker."""
import os
import time
import logging
import socket
from logging import StreamHandler
from subprocess import check_output, CalledProcessError
import psutil
import pyasn
from prometheus_client import Gauge, CollectorRegistry, generate_latest

def getStreamLogger(logLevel='DEBUG'):
    """ Get Stream Logger """
    levels = {'FATAL': logging.FATAL,
              'ERROR': logging.ERROR,
              'WARNING': logging.WARNING,
              'INFO': logging.INFO,
              'DEBUG': logging.DEBUG}
    logger = logging.getLogger()
    handler = StreamHandler()
    formatter = logging.Formatter("%(asctime)s.%(msecs)03d - %(name)s - %(levelname)s - %(message)s",
                                  datefmt="%a, %d %b %Y %H:%M:%S")
    handler.setFormatter(formatter)
    if not logger.handlers:
        logger.addHandler(handler)
    logger.setLevel(levels[logLevel])
    return logger

class XRootDLogMon:
    """ XRootD Log Monitoring Worker """
    def __init__(self, logger):
        self.logger = logger
        self.hostname = os.getenv('HOSTNAME', socket.gethostname())
        self.workdir = os.getenv('PROM_WORKDIR', "/srv/")
        self.registry = None
        self.loginGauge = None
        self.tpcPushGauge = None
        self.tpcPullGauge = None
        self.connectionGauge = None
        self.asndb = pyasn.pyasn('/opt/pyasn/GeoIPASNum.dat')
        self.xrootd_files =['/var/log/xrootd/xrootd.log',
                    '/var/log/xrootd/2/xrootd.log',
                    '/var/log/xrootd/3/xrootd.log',
                    '/var/log/xrootd/4/xrootd.log',
                    '/var/log/xrootd/clustered/xrootd.log',
                    '/var/log/xrootd/xcache/xrootd.log',
                    '/var/log/xrootd/stageout/xrootd.log']


    def __cleanRegistry(self):
        """Get new/clean prometheus registry."""
        self.registry = CollectorRegistry()

    def __cleanGauge(self):
        """Get new/clean prometheus gauge."""
        self.loginGauge = Gauge("xrootd_logins", "XRootD Logins",
                            ["hostname", "username"],
                            registry=self.registry)
        self.tpcPushGauge = Gauge("xrootd_tpc_push", "XRootD TPC Push Requests",
                            ["hostname", "event", "user"],
                            registry=self.registry)
        self.tpcPullGauge = Gauge("xrootd_tpc_pull", "XRootD TPC Pull Requests",
                            ["hostname", "event", "user"],
                            registry=self.registry)
        self.connectionGauge = Gauge("xrootd_connections", "XRootD Connections",
                            ["hostname", "laddr_asn", "raddr_asn", "iptype"],
                            registry=self.registry)

    def _executeCmd(self, cmd):
        """Execute Command"""
        stTime = int(time.time())
        out = b""
        try:
            self.logger.info(f"Call command {cmd}")
            out = check_output(cmd, shell=True)
            exCode = 0
            self.logger.debug(f'Got Exit: {exCode}, Cmd: {cmd}')
        except CalledProcessError as ex:
            exCode = ex.returncode
            self.logger.critical(f'Got Error: {ex}, Cmd: {cmd}')
        endTime = int(time.time())
        totalRuntime = endTime - stTime
        return out.decode('utf-8'), exCode, totalRuntime

    def getLogins(self):
        """Get Logins."""
        logins = {}
        for xfile in self.xrootd_files:
            if not os.path.isfile(xfile):
                continue
            # Get only last minute logins
            cmd = f'grep -E "(XrootdXeq|XrootdBridge)" {xfile} | grep "login as" | grep "$(date --date="1 minute ago" "+%H:%M")"'
            out, _, _ = self._executeCmd(cmd)
            # Count and get all unique usernames
            if out:
                for line in out.split('\n'):
                    tmpLine = line.split(' ')
                    logins.setdefault(tmpLine[-1], 0)
                    logins[tmpLine[-1]] += 1
        # Write to prometheus
        for user, count in logins.items():
            self.loginGauge.labels(self.hostname, user).set(count)

    def _parseTPCLine(self, line):
        """Parse TPC Line."""
        # Need to group all key=value pairs
        out = {}
        line = line.split(';')[0]  # Split out error, which goes after ;
        line = line.split(' ')
        for tmpline in line:
            if '=' in tmpline:
                key, value = tmpline.split('=')
                out[key] = value
        return out

    def parseTPCPushRequest(self):
        """Parse TPC Push Request."""
        allOut = {}
        for xfile in self.xrootd_files:
            if not os.path.isfile(xfile):
                continue
            cmd = f'grep -E "TPC_PushRequest" {xfile} | grep "$(date --date="1 minute ago" "+%H:%M")"'
            out, _, _ = self._executeCmd(cmd)
            if out:
                for line in out.split('\n'):
                    tpcOut = self._parseTPCLine(line)
                    if 'event' not in tpcOut or 'user' not in tpcOut:
                        continue
                    allOut.setdefault(tpcOut['event'], {})
                    allOut[tpcOut['event']].setdefault(tpcOut['user'], 0)
                    allOut[tpcOut['event']][tpcOut['user']] += 1
        # Write to prometheus
        for event, users in allOut.items():
            self.tpcPushGauge.labels(self.hostname, event, 'all').set(sum(users.values()))
            for user, count in users.items():
                self.tpcPushGauge.labels(self.hostname, event, user).set(count)

    def parseTPCPullRequest(self):
        """Parse TPC Pull Request."""
        allOut = {}
        for xfile in self.xrootd_files:
            if not os.path.isfile(xfile):
                continue
            cmd = f'grep -E "TPC_PullRequest" {xfile} | grep "$(date --date="1 minute ago" "+%H:%M")"'
            out, _, _ = self._executeCmd(cmd)
            if out:
                for line in out.split('\n'):
                    tpcOut = self._parseTPCLine(line)
                    if 'event' not in tpcOut or 'user' not in tpcOut:
                        continue
                    allOut.setdefault(tpcOut['event'], {})
                    allOut[tpcOut['event']].setdefault(tpcOut['user'], 0)
                    allOut[tpcOut['event']][tpcOut['user']] += 1
        # Write to prometheus
        for event, users in allOut.items():
            self.tpcPullGauge.labels(self.hostname, event, 'all').set(sum(users.values()))
            for user, count in users.items():
                self.tpcPullGauge.labels(self.hostname, event, user).set(count)

    def _getAsnType(self, ip):
        """Get ASN."""
        # IP can be ipv4/6. If IPv4 - need to cut out '::ffff:'
        # family always report AF_INET6, so need to check if it starts with ::ffff:
        iptype = '6'
        if ip.startswith('::ffff:'):
            iptype = '4'
            ip = ip.split('::ffff:')[1]
        asn = self.asndb.lookup(ip)[0]
        return iptype, asn

    def parseAllConnections(self):
        """Parse all connections"""
        # Get all active connections to port from env XRD_PORT (or default 1094)
        xrdPort = os.getenv('XRD_PORT', '1094')
        connections = {'4': {}, '6': {}}
        for conn in psutil.net_connections():
            if conn.laddr.port == int(xrdPort):
                # IP can be ipv4/6. If IPv4 - need to cut out '::ffff:'
                # family always report AF_INET6, so need to check if it starts with ::ffff:
                iptype = '6'
                try:
                    ip = conn.raddr.ip
                except AttributeError:
                    continue
                riptype, rasn = self._getAsnType(ip)
                try:
                    ip = conn.laddr.ip
                except AttributeError:
                    continue
                liptype, lasn = self._getAsnType(ip)
                if riptype != liptype:
                    print(f'How it can be? Ignoring. {liptype} {lasn} {riptype} {rasn}')
                    continue
                if rasn and lasn:
                    connections[liptype].setdefault(lasn, {})
                    connections[liptype][lasn].setdefault(rasn, 0)
                    connections[liptype][lasn][rasn] += 1
        # Write to prometheus
        for iptype, asns in connections.items():
            for lasn, rasns in asns.items():
                for rasn, count in rasns.items():
                    self.connectionGauge.labels(self.hostname, lasn, rasn, iptype).set(count)

    def main(self):
        """ Main Method"""
        self.__cleanRegistry()
        self.__cleanGauge()
        self.getLogins()
        self.parseTPCPushRequest()
        self.parseTPCPullRequest()
        self.parseAllConnections()

    def execute(self):
        """Execute Main Program."""
        startTime = int(time.time())
        self.logger.info('Running Main')
        self.main()
        endTime = int(time.time())
        totalRuntime = endTime - startTime
        data = generate_latest(self.registry)
        with open(f'{self.workdir}/xrootd-metrics', 'wb') as fd:
            fd.write(data)
        self.logger.info('StartTime: %s, EndTime: %s, Runtime: %s', startTime, endTime, totalRuntime)
        return totalRuntime


if __name__ == "__main__":
    LOGGER = getStreamLogger()
    xworker = XRootDLogMon(LOGGER)
    while True:
        runtimeAll = xworker.execute()
        sleepTime = int(60 - runtimeAll)
        if sleepTime > 0:
            LOGGER.info("Sleeping %s seconds", sleepTime)
            time.sleep(int(sleepTime))
