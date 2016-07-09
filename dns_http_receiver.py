#!/usr/bin/env python

import argparse
import zmq
import json
import requests
import datetime

class DnsIndexer(object):
    def __init__(self, es, index_name):
        self.es = es
        self.index_name = index_name

def main(probe_host, probe_port, http_host, http_port):
    print "Connecting to probe at tcp://{0}:{1}".format(probe_host, probe_port)

    # setup zmq connection
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect("tcp://{0}:{1}".format(probe_host, probe_port))
    socket.setsockopt(zmq.SUBSCRIBE, "dns")

    running = True

    # start receiving messages
    try:
        while running:
            msg = socket.recv()
            topic, data = msg.split(" ", 1)
            data = json.loads(data)
            del data["timestamp"]
            #timestamp = datetime.datetime.fromtimestamp(data["timestamp"])
            #data["timestamp"] = str(timestamp)
            print "Host: {0} Query: {1}".format(data["src_ip"], data["query"])
            requests.put("http://{0}:{1}/dns".format(http_host, http_port), json=data)


    except KeyboardInterrupt:
        running = False

    print "Stopping..."

if __name__ == "__main__":
    parser = argparse.ArgumentParser("Receiver for DnsProbe")

    parser.add_argument("-pp", "--probe-port", type=int, default=7777, help="port")
    parser.add_argument("-ph", "--probe-host", default="localhost", help="host")
    parser.add_argument("-eh", "--elastic-host", required=True, help="host with elasticsearch")
    parser.add_argument("-ep", "--elastic-port", type=int, default=9200, help="elastic port")

    args = parser.parse_args()
    main(args.probe_host,
         args.probe_port,
         args.elastic_host,
         args.elastic_port)
