FROM ubuntu:16.04
RUN apt-get update
RUN apt-get -y install python python-pip python-dev tcpdump
RUN pip install --upgrade pip
RUN pip install scapy pyzmq
COPY src /app
ENV IFACE eth0
ENV PORT  7777

EXPOSE ${PORT}
CMD /usr/bin/python /app/dns_probe.py --interface ${IFACE} --port ${PORT}
