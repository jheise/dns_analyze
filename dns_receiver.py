#!/usr/bin/env python

import argparse
import zmq
import json
import elasticsearch
import datetime

class DnsIndexer(object):
    def __init__(self, es, index_name):
        self.es = es
        self.index_name = index_name

def main(probe_host, probe_port, elastic_host, elastic_port):
    print "Connecting to probe at tcp://{0}:{1}".format(probe_host, probe_port)

    # setup zmq connection
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect("tcp://{0}:{1}".format(probe_host, probe_port))
    socket.setsockopt(zmq.SUBSCRIBE, "dns")

    print "Connecting to elasticsearch at {0}:{1}".format(elastic_host, elastic_port)
    es = elasticsearch.Elasticsearch("{0}:{1}".format(elastic_host, elastic_port))

    running = True

    # start receiving messages
    try:
        while running:
            msg = socket.recv()
            topic, data = msg.split(" ", 1)
            data = json.loads(data)
            timestamp = datetime.datetime.fromtimestamp(data["timestamp"])
            data["timestamp"] = timestamp
            print "Host: {0} Query: {1}".format(data["src_ip"], data["query"])
            es.create(index="dns-queries", doc_type="query", body=data)
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
