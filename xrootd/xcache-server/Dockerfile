FROM opensciencegrid/software-base:3.5-el8-release

# NOTES
# 2022 Mar 10th - Disable osg-upcoming, as it brings 5.x release with TLS.
#                 We are seeing a lot of TLS issue reading from Nebraska and Florida


ARG UNAME=xrootd
ARG UID=2010
ARG GID=2010
RUN groupadd -g $GID -o $UNAME
RUN useradd -m -u $UID -g $GID -o -s /bin/bash $UNAME

RUN yum -y install xrootd xrootd-client xrootd-client-devel xrootd-client-libs \
                   xrootd-devel xrootd-fuse xrootd-libs xrootd-private-devel \
                   xrootd-server xrootd-server-devel xrootd-server-libs xrootd-selinux \
                   xrootd-doc xrootd-lcmaps --enablerepo=osg-upcoming

RUN yum -y install xrootd-scitokens
RUN yum -y --disablerepo=* --enablerepo=epel update scitokens-cpp
