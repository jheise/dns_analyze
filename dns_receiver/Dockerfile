FROM resin/rpi-raspbian

RUN apt-get update
RUN apt-get install -y python-pip
RUN pip install --upgrade pip
RUN pip install scapy
COPY src /app

# setup env variables
ENV SOURCE_HOST 172.17.0.1
ENV SOURCE_PORT 7777
ENV ES_HOST 172.17.0.1
ENV ES_PORT 9200

CMD /app/dns_receiver.py -ph ${SOURCE_HOST} -pp ${SOURCE_PORT} -eh ${ES_HOST} -ep ${ES_PORT}
