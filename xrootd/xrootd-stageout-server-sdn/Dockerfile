FROM opensciencegrid/software-base:3.6-al8-release

ARG UNAME=xrootd
ARG UID=2010
ARG GID=2010
RUN groupadd -g $GID -o $UNAME
RUN useradd -m -u $UID -g $GID -o -s /bin/bash $UNAME

RUN cat /etc/yum.repos.d/*
RUN yum -y install xrootd xrootd-server xrootd-libs xrootd-server-libs xrootd-client xrootd-client-libs
RUN yum -y install xrootd-scitokens python3-scitokens gfal2-plugin-xrootd xrootd-multiuser xrootd-voms
RUN yum -y install voms-clients

RUN mkdir -p /var/log/xrootd/clustered/
RUN chown -R xrootd:xrootd /var/log/xrootd/

# Install custom monitoring
RUN yum -y install net-tools git wget
RUN mkdir -p /opt
RUN cd /opt/ && git clone https://github.com/juztas/t2_maitenance
RUN cd /opt/t2_maitenance && pip3 install -r requirements.txt
RUN cd /opt/t2_maitenance && python3 setup.py install

# Add cron to fetch crl on boot
ADD config/default/etc/cron.d/fetch-crl-reboot /etc/cron.d/fetch-crl-reboot

ADD config/default/etc/supervisord.d/10-xrootd.conf /etc/supervisord.d/10-xrootd.conf
ADD config/default/etc/xrootd/scitokens.cfg /etc/xrootd/scitokens.cfg
ADD config/default/etc/xrootd/robots.txt /etc/xrootd/robots.txt
ADD config/default/etc/xrootd/xrootd-clustered.cfg /etc/xrootd/xrootd-clustered.cfg
ADD config/default/etc/xrootd/auth_file /etc/xrootd/auth_file
ADD config/default/etc/sense-cleaner.sh /etc/sense-cleaner.sh
ADD config/default/etc/cron.d/sense-cleaner /etc/cron.d/sense-cleaner

# Add Custom checksum file (needed for Rucio tests and tmpfs, which does not support xattr)
ADD config/default/etc/xrootd/checksum.py /etc/xrootd/checksum.py

# Allow CMS VO Users to communicate;
RUN mkdir -p /etc/grid-security/vomsdir/cms/
ADD config/default/etc/grid-security/vomsdir/cms/lcg-voms2.cern.ch.lsc /etc/grid-security/vomsdir/cms/lcg-voms2.cern.ch.lsc
ADD config/default/etc/grid-security/vomsdir/cms/voms-cms-auth.app.cern.ch.lsc /etc/grid-security/vomsdir/cms/voms-cms-auth.app.cern.ch.lsc
ADD config/default/etc/grid-security/vomsdir/cms/voms2.cern.ch.lsc /etc/grid-security/vomsdir/cms/voms2.cern.ch.lsc

# Add default grid and voms mapfile
ADD config/default/etc/grid-security/grid-mapfile /etc/grid-security/grid-mapfile
ADD config/default/etc/grid-security/voms-mapfile /etc/grid-security/voms-mapfile

# Get latest CA's
RUN fetch-crl || echo "Supress warnings."
