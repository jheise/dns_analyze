FROM ubuntu:16.04
RUN apt-get update
RUN apt-get -y install python python-pip python-dev
RUN pip install --upgrade pip
RUN pip install pyzmq requests
COPY src /app
ENV ZMQ tcp://localhost:7777
ENV TOPIC dns
ENV GELF http://localhost:9500/gelf
ENV HOST dns_scan

CMD /usr/bin/python /app/dns_gelf.py --zmq ${ZMQ} --topic ${TOPIC} --gelf ${GELF} --host ${HOST}
