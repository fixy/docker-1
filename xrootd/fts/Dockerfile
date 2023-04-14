FROM docker.io/rucio/fts

RUN yum -y install voms-clients fetch-crl wget
RUN yum -y install https://repo.opensciencegrid.org/osg/3.6/osg-3.6-el7-release-latest.rpm
RUN yum -y install osg-ca-certs

# Add cron to fetch crl on boot
ADD config/default/etc/cron.d/fetch-crl-reboot /etc/cron.d/fetch-crl-reboot

# Add httpd conf
ADD config/default/etc/httpd/conf.d/fts3rest.conf /etc/httpd/conf.d/fts3rest.conf
ADD config/default/etc/httpd/conf.d/ftsmon.conf /etc/httpd/conf.d/ftsmon.conf
ADD config/default/etc/fts3/fts3config /etc/fts3/fts3config

# Add Runtime script
ADD config/default/docker-entrypoint.sh /docker-entrypoint.sh

# Allow CMS VO Users to communicate;
RUN mkdir -p /etc/grid-security/vomsdir/cms/
ADD config/default/etc/grid-security/vomsdir/cms/lcg-voms2.cern.ch.lsc /etc/grid-security/vomsdir/cms/lcg-voms2.cern.ch.lsc
ADD config/default/etc/grid-security/vomsdir/cms/voms-cms-auth.app.cern.ch.lsc /etc/grid-security/vomsdir/cms/voms-cms-auth.app.cern.ch.lsc
ADD config/default/etc/grid-security/vomsdir/cms/voms2.cern.ch.lsc /etc/grid-security/vomsdir/cms/voms2.cern.ch.lsc

# Get latest CA's
RUN fetch-crl || echo "Supress warnings."
