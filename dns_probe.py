#!/usr/bin/env python

import argparse
import zmq
import time
import json
from scapy.all import *

class DnsProbe(object):

    def __init__(self, socket):
        super(DnsProbe, self).__init__()
        self.socket = socket
        self.running = True

    def process(self):
        while self.running:
            sniff(filter="udp and port 53", prn=self.check_packet, count=1, store=0)

    def check_packet(self, pkt):

        src_ip = pkt[IP].src
        query = pkt[DNS].qd.qname
        captured = time.time()
        data = {"src_ip":src_ip,
                "query":query,
                "timestamp":captured}

        output = json.dumps(data)
        print output
        self.socket.send("dns " + output)

def main(interface, port):
    print "Starting capture on {0}".format(interface)

    # set the given interface
    conf.iface = interface

    # setup the zmq pub socket
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://*:{0}".format(port))

    dnsprobe = DnsProbe(socket)

    try:
        print "scanning for dns requests..."
        #sniff(filter="udp and port 53", prn=check_packet, count=10, store=0)
        dnsprobe.process()
    except KeyboardInterrupt:
        print "Stopping..."
        dnsprobe.running = False

if __name__ == "__main__":

    parser = argparse.ArgumentParser("Script to analyze incoming DNS traffic")
    parser.add_argument("-i", "--interface", default="eth0", help="Interface to use")
    parser.add_argument("-p", "--port", default=7777, type=int, help="port to bind")

    args = parser.parse_args()

    main(args.interface, args.port)
