#!/bin/bash
mkdir -p /etc/grid-security/xrootd/
cp /etc/grid-security/xrootdcert.pem $XRD_CERT
cp /etc/grid-security/xrootdkey.pem $XRD_KEY
chown xrootd:xrootd $XRD_CERT
chown xrootd:xrootd $XRD_KEY
chmod 600 $XRD_KEY
while :
do
  if cmp --silent -- "$X509_USER_PROXY" "$K8S_X509_USER_PROXY"; then
    echo "XCache Proxy is same. No need to update. sleep 10mins"
  else
    echo "XCache proxy was updated. Updating X509..."
    cp $K8S_X509_USER_PROXY $X509_USER_PROXY
    chown xrootd:xrootd $X509_USER_PROXY
    chmod 600 $X509_USER_PROXY
    echo "New Proxy details:"
    voms-proxy-info -all
    echo "Update done. Sleep 10 mins"
  fi
  sleep 600
done


