ARG RELEASE=latest
FROM cmscaltech/base_image:$RELEASE
# NOTES
# 2022 Mar 10th - Disable osg-upcoming, as it brings 5.x release with TLS.
#                 We are seeing a lot of TLS issue reading from Nebraska and Florida
# 2023 Dec 15th - Move to OSG 23 AlmaLinux 8 Release
# 2024 Feb 7th - Move to cmscaltech/base_image (which is based on OSG Image. See base_image repo)

ARG UNAME=xrootd
ARG UID=2010
ARG GID=2010
RUN groupadd -g $GID -o $UNAME && \
    useradd -l -m -u $UID -g $GID -o -s /bin/bash $UNAME

RUN yum -y install xrootd xrootd-client xrootd-client-devel xrootd-client-libs \
                   xrootd-devel xrootd-fuse xrootd-libs xrootd-private-devel \
                   xrootd-server xrootd-server-devel xrootd-server-libs xrootd-selinux \
                   xrootd-voms voms-clients xrootd-doc xrootd-scitokens scitokens-cpp && yum clean all

RUN mkdir -p /var/log/xrootd/clustered/ && \
    chown -R xrootd:xrootd /var/log/xrootd/ && \
    mkdir -p /etc/grid-security/mapfile/

# XCache Rucio reporter. Installing it manually
#RUN yum -y install git procps-ng && yum clean all
#RUN cd /opt && git clone https://github.com/juztas/xcache

# Install custom monitoring
RUN pip3 install prometheus_client flask
COPY config/default/opt/xroot-mon.py /opt/xroot-mon.py
COPY config/default/opt/http-server.py /opt/http-server.py

# To track connections, we need pyasn lib and GeoIP database
RUN yum -y install gcc python3-devel python3-gunicorn && yum clean all
RUN pip3 install pyasn psutil
RUN mkdir -p /opt/pyasn
RUN pyasn_util_download.py --latestv46 --filename /opt/pyasn/GeoIPASNum.rib && \
    pyasn_util_convert.py --single /opt/pyasn/GeoIPASNum.rib /opt/pyasn/GeoIPASNum.dat && \
    rm -f /opt/pyasn/GeoIPASNum.rib

# Add Supervisor.d and xrootd configs
COPY config/default/etc/supervisord.d/10-xrootd.conf /etc/supervisord.d/10-xrootd.conf
COPY config/default/etc/xrootd/auth_file /etc/xrootd/auth_file
COPY config/default/etc/xrootd/xrootd.cfg /etc/xrootd/xrootd.cfg
COPY config/default/etc/xrootd/robots.txt /etc/xrootd/robots.txt
COPY config/default/etc/xrootd/scitokens.cfg /etc/xrootd/scitokens.cfg
COPY config/default/usr/local/sbin/startup.sh /usr/local/sbin/startup.sh
RUN chmod +x /usr/local/sbin/startup.sh

# Allow CMS VO Users to communicate;
RUN mkdir -p /etc/grid-security/vomsdir/cms/
COPY config/default/etc/grid-security/vomsdir/cms/lcg-voms2.cern.ch.lsc /etc/grid-security/vomsdir/cms/lcg-voms2.cern.ch.lsc
COPY config/default/etc/grid-security/vomsdir/cms/voms-cms-auth.app.cern.ch.lsc /etc/grid-security/vomsdir/cms/voms-cms-auth.app.cern.ch.lsc
COPY config/default/etc/grid-security/vomsdir/cms/voms2.cern.ch.lsc /etc/grid-security/vomsdir/cms/voms2.cern.ch.lsc

# Add default grid and voms mapfile
COPY config/default/etc/grid-security/mapfile/grid-mapfile /etc/grid-security/mapfile/grid-mapfile
COPY config/default/etc/grid-security/mapfile/voms-mapfile /etc/grid-security/mapfile/voms-mapfile

# Add cron to fetch crl on boot
COPY config/default/etc/cron.d/fetch-crl-reboot /etc/cron.d/fetch-crl-reboot

# Get latest CA's
RUN fetch-crl || echo "Supress warnings."
