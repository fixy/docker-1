FROM opensciencegrid/software-base:3.5-el8-release

ARG UNAME=xrootd
ARG UID=2010
ARG GID=2010
RUN groupadd -g $GID -o $UNAME
RUN useradd -m -u $UID -g $GID -o -s /bin/bash $UNAME

RUN yum -y install xrootd xrootd-client xrootd-client-devel xrootd-client-libs \
                   xrootd-devel xrootd-fuse xrootd-libs xrootd-private-devel \
                   xrootd-server xrootd-server-devel xrootd-server-libs xrootd-selinux \
                   xrootd-doc xrootd-lcmaps --enablerepo=osg-upcoming

