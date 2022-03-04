FROM opensciencegrid/osg-wn:3.5-el8
# Notes:
# Cloned from Nebraska folks: https://github.com/unlhcc/docker-osg-wn-el7
#
# Modifications:
# - 2022-Feb-09: Change FROM el7 to el8
# - 2022-Feb-09: Removed compat-libstdc++-33, coreutils
# - 2022-Mar-02: Add bind-utils and openssl-libs packages
# - 2022-Mar-02: Add compat-openssl10 (needed for CMS pilots in EL8)
# - 2022-Mar-03: Install python2 and symlink (CMS SAM depends on python2)
#                Move python symlink at the end (yum update install python3 and removes symlink)
#                See https://developers.redhat.com/blog/2019/05/07/what-no-python-in-red-hat-enterprise-linux-8
#
# Required
# --------
# - cmsRun fails without stdint.h (from glibc-headers)
#   Tested CMSSW_7_4_5_patch1
#
# Other
# -----
# - ETF calls /usr/bin/lsb_release (from redhat-lsb-core)
# - sssd-client for LDAP lookups through the host
# - SAM tests expect cvmfs utilities
# - gcc is required by GLOW jobs (builds matplotlib)
#
# CMSSW dependencies
# ------------------
# Required software is listed under slc7_amd64_platformSeeds at
# http://cmsrep.cern.ch/cgi-bin/cmspkg/driver/cms/slc7_amd64_gcc700

RUN yum -y install cvmfs \
                   gcc \
                   glibc-headers \
                   openssh-clients \
                   osg-wn-client \
                   redhat-lsb-core \
                   sssd-client && \
    yum -y install glibc bash tcsh zsh perl tcl tk readline openssl \
                   ncurses e2fsprogs krb5-libs freetype ncurses-libs perl-libs \
                   perl-ExtUtils-Embed fontconfig libidn \
                   libX11 libXmu libSM libICE libXcursor libXext libXrandr \
                   libXft mesa-libGLU mesa-libGL e2fsprogs-libs libXi \
                   libXinerama libXft-devel libXrender libXpm libcom_err \
                   perl-Test-Harness perl-Carp perl-constant perl-PathTools \
                   perl-Data-Dumper perl-Digest-MD5 perl-Exporter \
                   perl-File-Path perl-File-Temp perl-Getopt-Long perl-Socket \
                   perl-Text-ParseWords perl-Time-Local libX11-devel \
                   libXpm-devel libXext-devel mesa-libGLU-devel perl-Switch \
                   perl-Storable perl-Env perl-Thread-Queue perl-Encode nspr \
                   nss nss-util file file-libs readline zlib popt bzip2 \
                   bzip2-libs bind-utils openssl-libs compat-openssl10 python2 && \
    yum clean all && \
    rm -rf /var/cache/yum

# Create condor user and group
RUN groupadd -r condor && \
    useradd -r -g condor -d /var/lib/condor -s /sbin/nologin condor

# Sync singularity version
RUN yum -y distro-sync --enablerepo=epel-testing singularity && \
    yum clean all && \
    rm -rf /var/cache/yum

# Disable overlay and privileged mode
RUN perl -pi -e 's/^enable overlay =.*/enable overlay = no/g' /etc/singularity/singularity.conf && \
    perl -pi -e 's/^allow setuid =.*/allow setuid = no/g'     /etc/singularity/singularity.conf

# yum update
RUN yum update -y && \
    yum clean all && \
    rm -rf /var/cache/yum

RUN ln -s /usr/bin/python2 /usr/bin/python
