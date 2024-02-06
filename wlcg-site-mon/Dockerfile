FROM opensciencegrid/software-base:23-al8-release

RUN yum install -y vim net-snmp git net-snmp-devel python3-devel gcc net-snmp-utils && yum clean all

RUN pip3 install easysnmp==0.2.5

ADD config/10-wlcg-mon.conf /etc/supervisord.d/10-wlcg-mon.conf

ADD config/WLCG-site-snmp-http.py /opt/WLCG-site-snmp-http.py

# Expose any ports that your application may use
EXPOSE 443 80
