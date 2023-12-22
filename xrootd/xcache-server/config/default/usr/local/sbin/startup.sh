#!/bin/bash
mkdir -p /etc/grid-security/xrootd/
cp /etc/grid-security/xrootdcert.pem $XRD_CERT
cp /etc/grid-security/xrootdkey.pem $XRD_KEY
chown xrootd:xrootd $XRD_CERT
chown xrootd:xrootd $XRD_KEY
chmod 600 $XRD_KEY

