FROM resin/rpi-raspbian
RUN apt-get update
RUN apt-get -y install python tcpdump python-zmq python-scapy
COPY ../src /app

ENV IFACE eth0
ENV PORT  7777

EXPOSE ${PORT}
CMD /usr/bin/python /app/dns_probe.py --interface ${IFACE} --port ${PORT}
