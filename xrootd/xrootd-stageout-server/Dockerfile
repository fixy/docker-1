FROM opensciencegrid/software-base:3.5-el8-release

ARG UNAME=xrootd
ARG UID=2010
ARG GID=2010
RUN groupadd -g $GID -o $UNAME
RUN useradd -m -u $UID -g $GID -o -s /bin/bash $UNAME

RUN yum -y install xrootd xrootd-server xrootd-libs xrootd-server-libs xrootd-client xrootd-client-libs --enablerepo=osg-upcoming
RUN yum -y install xrootd-scitokens python3-scitokens gfal2-plugin-xrootd xrootd-multiuser xrootd-lcmaps --enablerepo=osg-upcoming

RUN mkdir -p /var/log/xrootd/clustered/
RUN chown -R xrootd:xrootd /var/log/xrootd/

# Install custom monitoring
RUN yum -y install net-tools git
RUN mkdir -p /opt
RUN cd /opt/ && git clone https://github.com/juztas/t2_maitenance
RUN cd /opt/t2_maitenance && pip3 install -r requirements.txt
RUN cd /opt/t2_maitenance && python3 setup.py install
