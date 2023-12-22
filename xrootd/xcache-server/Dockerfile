FROM opensciencegrid/software-base:23-al8-release
# NOTES
# 2022 Mar 10th - Disable osg-upcoming, as it brings 5.x release with TLS.
#                 We are seeing a lot of TLS issue reading from Nebraska and Florida
# 2023 Dec 15th - Move to OSG 23 AlmaLinux 8 Release

ARG UNAME=xrootd
ARG UID=2010
ARG GID=2010
RUN groupadd -g $GID -o $UNAME
RUN useradd -m -u $UID -g $GID -o -s /bin/bash $UNAME

RUN yum -y install xrootd xrootd-client xrootd-client-devel xrootd-client-libs \
                   xrootd-devel xrootd-fuse xrootd-libs xrootd-private-devel \
                   xrootd-server xrootd-server-devel xrootd-server-libs xrootd-selinux \
                   xrootd-voms voms-clients xrootd-doc xrootd-scitokens scitokens-cpp && yum clean all

RUN mkdir -p /var/log/xrootd/clustered/
RUN chown -R xrootd:xrootd /var/log/xrootd/

# XCache Rucio reporter. Installing it manually
RUN yum -y install git procps-ng && yum clean all
RUN cd /opt && git clone https://github.com/juztas/xcache

# Install custom monitoring
RUN yum -y install net-tools iproute git wget && yum clean all
RUN mkdir -p /opt
RUN cd /opt/ && git clone https://github.com/juztas/t2_maitenance
RUN cd /opt/t2_maitenance && pip3 install -r requirements.txt
RUN cd /opt/t2_maitenance && python3 setup.py install

# Add Supervisor.d and xrootd configsc
ADD config/default/etc/supervisord.d/10-xrootd.conf /etc/supervisord.d/10-xrootd.conf
ADD config/default/etc/xrootd/auth_file /etc/xrootd/auth_file
ADD config/default/etc/xrootd/xrootd.cfg /etc/xrootd/xrootd.cfg
ADD config/default/etc/xrootd/robots.txt /etc/xrootd/robots.txt
ADD config/default/etc/xrootd/scitokens.cfg /etc/xrootd/scitokens.cfg

# Allow CMS VO Users to communicate;
RUN mkdir -p /etc/grid-security/vomsdir/cms/
ADD config/default/etc/grid-security/vomsdir/cms/lcg-voms2.cern.ch.lsc /etc/grid-security/vomsdir/cms/lcg-voms2.cern.ch.lsc
ADD config/default/etc/grid-security/vomsdir/cms/voms-cms-auth.app.cern.ch.lsc /etc/grid-security/vomsdir/cms/voms-cms-auth.app.cern.ch.lsc
ADD config/default/etc/grid-security/vomsdir/cms/voms2.cern.ch.lsc /etc/grid-security/vomsdir/cms/voms2.cern.ch.lsc

# Add default grid and voms mapfile
ADD config/default/etc/grid-security/grid-mapfile /etc/grid-security/grid-mapfile
ADD config/default/etc/grid-security/voms-mapfile /etc/grid-security/voms-mapfile

# Add cron to fetch crl on boot
ADD config/default/etc/cron.d/fetch-crl-reboot /etc/cron.d/fetch-crl-reboot

# Get latest CA's
RUN fetch-crl || echo "Supress warnings."
