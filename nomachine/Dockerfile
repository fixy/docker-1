FROM ubuntu:16.04

ENV DEBIAN_FRONTEND=noninteractive

# Configure timezone and locale to spanish and America/Bogota timezone. Change locale and timezone to whatever you want
ENV LANG="en_US.UTF-8"
ENV LANGUAGE=en_US

# Goto https://www.nomachine.com/download/download&id=10 and change for the latest NOMACHINE_PACKAGE_NAME and MD5 shown in that link to get the latest version.
ENV NOMACHINE_PACKAGE_NAME nomachine_6.2.4_1_amd64.deb
ENV NOMACHINE_BUILD 6.2
ENV NOMACHINE_MD5 210bc249ec9940721a1413392eee06fe

RUN apt-get clean && apt-get update && apt-get install -y locales && \
    locale-gen en_US.UTF-8 && locale-gen en_US && \
    echo "America/New_York" > /etc/timezone && \
    apt-get install -y locales && \
    sed -i -e "s/# $LANG.*/$LANG.UTF-8 UTF-8/" /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales && \
    update-locale LANG=$LANG && \
    apt-get update -y && \
    apt-get install -y software-properties-common python-software-properties python3-software-properties sudo && \
    add-apt-repository universe && \
    apt-get update -y && \
    
    apt-get install -y xterm pulseaudio cups curl \
    libgconf2-4 iputils-ping libnss3-1d libxss1 wget xdg-utils libpango1.0-0 fonts-liberation \
    mate-desktop-environment-extras firefox htop nano git vim && \
    
    curl -fSL "http://download.nomachine.com/download/${NOMACHINE_BUILD}/Linux/${NOMACHINE_PACKAGE_NAME}" -o nomachine.deb \
&& echo "${NOMACHINE_MD5} *nomachine.deb" | md5sum -c - && dpkg -i nomachine.deb && sed -i "s|#EnableClipboard both|EnableClipboard both |g" /usr/NX/etc/server.cfg

ADD nxserver.sh /

ENTRYPOINT ["/nxserver.sh"]
