FROM ubuntu:16.04
RUN apt-get update
RUN apt-get -y install python python-pip python-dev
RUN pip install --upgrade pip
RUN pip install pyzmq
COPY src /app

ENV SIP    10.0.0.1
ENV SPORT  7777
ENV PORT   7777

EXPOSE ${PORT}
CMD /usr/bin/python /app/dns_threat.py --source_address ${SIP} --source_port ${SPORT} --port ${PORT}
