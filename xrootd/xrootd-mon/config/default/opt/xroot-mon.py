#!/usr/bin/env python3
import os
import time
import logging
from logging import StreamHandler
from subprocess import check_output, CalledProcessError
from datetime import datetime
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

class XRootDCache:
    """ XRootD Cache Worker """
    def __init__(self, logger):
        self.logger = logger
        self.prevdatetime = None
        self.currdatetime = None
        self.params = self._getParams()
        self.workdir = self.params['XRD_WORKDIR']
        self.lfn = None
        self.registry = None
        self.gauge = None
        self.runtimeGauge = None

    def __cleanRegistry(self):
        """Get new/clean prometheus registry."""
        self.registry = CollectorRegistry()

    def __cleanGauge(self):
        """Get new/clean prometheus gauge."""
        self.gauge = Gauge("xrootd_exit", "XRootD Exit Code",
                            ["hostname", "mode", "protocol", "name"],
                            registry=self.registry)
        self.runtimeGauge = Gauge("xrootd_runtime", "XRootD Command Runtime",
                                    ["hostname", "mode", "protocol", "name"],
                                    registry=self.registry)

    def _getLabels(self, hostname, mode, protocol):
        """Get Labels for Prometheus Gauge."""
        return {"hostname": hostname, "mode": mode,
                "protocol": protocol, "name": self.params['XRD_UNIQ_NAME']}

    def _getParams(self):
        out = {}
        # Mandatory ENV Variables
        for key in ['XRD_ENDPOINT', 'X509_USER_PROXY',
                    'XRD_WORKDIR', 'XRD_UNIQ_NAME',
                    'XRD_PATH']:
            out[key] = os.environ.get(key)
            if not out[key]:
                raise Exception(f'ENV Variable {key} not found. Fatal Error. Exiting.')
        for key in ['XRD_PROTOCOLS', 'XRD_MODES']:
            out[key] = os.environ.get(key)
            if ',' in out[key]:
                out[key] = out[key].split(',')
            else:
                out[key] = [out[key]]
        # Optional ENV Variables
        tmpKey = os.environ.get('XRD_UNIQ_WRITE')
        if tmpKey:
            out['XRD_UNIQ_WRITE'] = bool(tmpKey)
        else:
            out['XRD_UNIQ_WRITE'] = False
        return out

    def _getLFN(self):
        """Get LFN"""
        currdate = self.currdatetime
        currLFN = '%s/%s/%s/%s/%s-cache-test-%s' % (self.params['XRD_PATH'],currdate.year,
                                                    currdate.month, currdate.day,
                                                    currdate.hour, self.params['XRD_UNIQ_NAME'])
        if 'cache' in self.params['XRD_MODES']:
            currLFN = '%s/%s/%s/%s/%s-cache-test' % (self.params['XRD_PATH'], currdate.year,
                                                        currdate.month, currdate.day,
                                                        currdate.hour)
        if 'write' not in self.params['XRD_MODES'] and 'read' in self.params['XRD_MODES']:
            currLFN = '%s/%s/%s/%s/%s-cache-test' % (self.params['XRD_PATH'], currdate.year,
                                                        currdate.month, currdate.day,
                                                        currdate.hour)
        self.lfn = currLFN

    def _executeCmd(self, cmd):
        """Execute Command"""
        stTime = int(time.time())
        out = None
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
        return out, exCode, totalRuntime

    def _writeFile(self, protocol, hostname):
        """Write File to XRootD"""
        cmd = f"timeout 30 gfal-copy -p -f {self.workdir}/xrd-cache-test {protocol}://{hostname}/{self.lfn}-{hostname}"
        _, exitCode, runtime = self._executeCmd(cmd)
        self.gauge.labels(**self._getLabels(hostname, "write", protocol)).set(exitCode)
        self.runtimeGauge.labels(**self._getLabels(hostname, "write", protocol)).set(runtime)
        return exitCode

    def preparefiles(self):
        """ Prepare Files for xrdcp"""
        if 'write' not in self.params['XRD_MODES']:
            return []
        content = f"This is a test file for xrdcp, created at {self.currdatetime}"
        if os.path.isfile(f'{self.workdir}/xrd-cache-test'):
            os.remove(f'{self.workdir}/xrd-cache-test')
        with open(f'{self.workdir}/xrd-cache-test', 'w', encoding='utf-8') as fd:
            fd.write(content)
        exitCodes = []
        for protocol in self.params['XRD_PROTOCOLS']:
            exitCode = self._writeFile(protocol, self.params['XRD_ENDPOINT'])
            exitCodes.append(exitCode)
        if not any(exitCodes):
            self.prevdatetime = self.currdatetime
        return exitCodes

    def main(self):
        """ Main Method"""
        self.__cleanRegistry()
        self.__cleanGauge()
        self.currdatetime = datetime.utcnow()
        self._getLFN()
        self.preparefiles()
        cmd = f"timeout 30 xrdmapc --list all {self.params['XRD_ENDPOINT']}"
        # xrdmapc --list all xcache.ultralight.org:2040
        # returns output as byte string
        self.logger.info('Calling %s', cmd)
        retOutput = []
        retOutput, exitCode, runtime = self._executeCmd(cmd)
        self.gauge.labels(**self._getLabels(self.params['XRD_ENDPOINT'], "xrdmapc", "xrootd")).set(exitCode)
        self.runtimeGauge.labels(**self._getLabels(self.params['XRD_ENDPOINT'], "xrdmapc", "xrootd")).set(runtime)
        if exitCode:
            return
        self.logger.info(f"Returned out from Redirector: {retOutput}")
        for line in retOutput.decode("utf-8").split('\n'):
            if not line:
                break
            line = line.strip()
            if line.startswith('Srv '):
                host = line.split()[1]
            else:
                self.logger.debug(f"Skipping line: {line}")
                continue
            if 'write' in self.params['XRD_MODES'] and self.params['XRD_UNIQ_WRITE']:
                for protocol in self.params['XRD_PROTOCOLS']:
                    self._writeFile(protocol, host)
            if 'read' in self.params['XRD_MODES']:
                for protocol in self.params['XRD_PROTOCOLS']:
                    cmd = f"timeout 30 gfal-copy -f {protocol}://{host}/{self.lfn} /dev/null"
                    _, exitCode, runtime = self._executeCmd(cmd)
                    self.gauge.labels(**self._getLabels(host, "read", protocol)).set(exitCode)
                    self.runtimeGauge.labels(**self._getLabels(host, "read", protocol)).set(runtime)
            if 'cache' in self.params['XRD_MODES']:
                for protocol in self.params['XRD_PROTOCOLS']:
                    cmd = f"timeout 30 gfal-copy -f {protocol}://{host}/{self.lfn} {self.workdir}/xrd-cache-test"
                    _, exitCode, runtime = self._executeCmd(cmd)
                    self.gauge.labels(**self._getLabels(host, "cache", protocol)).set(exitCode)
                    self.runtimeGauge.labels(**self._getLabels(host, "cache", protocol)).set(runtime)

    def execute(self):
        """Execute Main Program."""
        startTime = int(time.time())
        self.logger.info('Running Main')
        self.main()
        endTime = int(time.time())
        totalRuntime = endTime - startTime
        self.runtimeGauge.labels(**self._getLabels('MAIN_PROGRAM', "main", "xrootd")).set(totalRuntime)
        data = generate_latest(self.registry)
        with open(f'{self.workdir}/xrootd-metrics', 'wb') as fd:
            fd.write(data)
        self.logger.info('StartTime: %s, EndTime: %s, Runtime: %s', startTime, endTime, totalRuntime)
        return totalRuntime


if __name__ == "__main__":
    LOGGER = getStreamLogger()
    xcacheWorker = XRootDCache(LOGGER)
    while True:
        runtimeAll = xcacheWorker.execute()
        sleepTime = int(300 - runtimeAll)
        if sleepTime > 0:
            LOGGER.info("Sleeping %s seconds", sleepTime)
            time.sleep(int(sleepTime))
