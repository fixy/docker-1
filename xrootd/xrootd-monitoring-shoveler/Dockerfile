FROM opensciencegrid/software-base:3.6-el8-release

ARG UNAME=xrootd
ARG UID=2010
ARG GID=2010
RUN groupadd -g $GID -o $UNAME
RUN useradd -m -u $UID -g $GID -o -s /bin/bash $UNAME

RUN yum -y install xrootd-monitoring-shoveler
COPY config/default/etc/supervisord.d/10-xrootd-monitoring-shoveler.conf /etc/supervisord.d/10-xrootd-monitoring-shoveler.conf
COPY config/default/etc/osg/image-init.d/55-xrootd-monitoring-shoveler.sh /etc/osg/image-init.d/55-xrootd-monitoring-shoveler.sh
RUN chmod +x /etc/osg/image-init.d/55-xrootd-monitoring-shoveler.sh

RUN chown -R xrootd:xrootd /etc/xrootd-monitoring-shoveler/
RUN chmod -R 600 /etc/xrootd-monitoring-shoveler
RUN chmod    700 /etc/xrootd-monitoring-shoveler
