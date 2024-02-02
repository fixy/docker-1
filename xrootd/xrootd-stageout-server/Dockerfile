FROM opensciencegrid/software-base:23-al8-release

ARG UNAME=xrootd
ARG UID=2010
ARG GID=2010
RUN groupadd -g $GID -o $UNAME
RUN useradd -m -u $UID -g $GID -o -s /bin/bash $UNAME


RUN yum -y install xrootd xrootd-server xrootd-libs xrootd-server-libs xrootd-client \
                   xrootd-client-libs xrootd-scitokens python3-scitokens gfal2-plugin-xrootd \
                   xrootd-multiuser xrootd-voms voms-clients && yum clean all

RUN mkdir -p /var/log/xrootd/clustered/
RUN chown -R xrootd:xrootd /var/log/xrootd/

# Install custom monitoring
RUN pip3 install prometheus_client flask
COPY config/default/etc/supervisord.d/10-xrootd.conf /etc/supervisord.d/10-xrootd.conf
COPY config/default/opt/xroot-mon.py /opt/xroot-mon.py
COPY config/default/opt/http-server.py /opt/http-server.py

# To track connections, we need pyasn lib and GeoIP database
RUN yum -y install gcc python3-devel python3-gunicorn && yum clean all
RUN pip3 install pyasn psutil
RUN mkdir -p /opt/pyasn
RUN pyasn_util_download.py --latestv46 --filename /opt/pyasn/GeoIPASNum.rib && \
    pyasn_util_convert.py --single /opt/pyasn/GeoIPASNum.rib /opt/pyasn/GeoIPASNum.dat && \
    rm -f /opt/pyasn/GeoIPASNum.rib

# Add cron to fetch crl on boot
COPY config/default/etc/cron.d/fetch-crl-reboot /etc/cron.d/fetch-crl-reboot

COPY config/default/etc/supervisord.d/10-xrootd.conf /etc/supervisord.d/10-xrootd.conf
COPY config/default/etc/xrootd/scitokens.cfg /etc/xrootd/scitokens.cfg
COPY config/default/etc/xrootd/robots.txt /etc/xrootd/robots.txt
COPY config/default/etc/xrootd/xrootd-clustered.cfg /etc/xrootd/xrootd-clustered.cfg
COPY config/default/etc/xrootd/auth_file /etc/xrootd/auth_file

# Add Custom checksum file (needed for Rucio tests and tmpfs, which does not support xattr)
COPY config/default/etc/xrootd/checksum.py /etc/xrootd/checksum.py

# Allow CMS VO Users to communicate;
RUN mkdir -p /etc/grid-security/vomsdir/cms/
COPY config/default/etc/grid-security/vomsdir/cms/lcg-voms2.cern.ch.lsc /etc/grid-security/vomsdir/cms/lcg-voms2.cern.ch.lsc
COPY config/default/etc/grid-security/vomsdir/cms/voms-cms-auth.app.cern.ch.lsc /etc/grid-security/vomsdir/cms/voms-cms-auth.app.cern.ch.lsc
COPY config/default/etc/grid-security/vomsdir/cms/voms2.cern.ch.lsc /etc/grid-security/vomsdir/cms/voms2.cern.ch.lsc

# Add default grid and voms mapfile
COPY config/default/etc/grid-security/grid-mapfile /etc/grid-security/grid-mapfile
COPY config/default/etc/grid-security/voms-mapfile /etc/grid-security/voms-mapfile

# Get latest CA's
RUN fetch-crl || echo "Supress warnings."
