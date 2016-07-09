#!/usr/bin/env python

import argparse
from scapy.all import *

#known_dns = []

def check_packet(pkt):
    global known_dns

    src_ip = pkt[IP].src
    query = pkt[DNS].qd.qname
    #if query not in known_dns:
        #known_dns.append(query)
    print "Src: {0} Query: {1}".format(src_ip, query)

def main(interface):
    print "Starting capture on {0}".format(interface)
    conf.iface = interface

    try:
        print "scanning for dns requests..."
        #sniff(filter="udp and port 53", prn=check_packet, count=10, store=0)
        sniff(filter="udp and port 53", prn=check_packet, store=0)
    except KeyboardInterrupt:
        exit(0)

if __name__ == "__main__":

    parser = argparse.ArgumentParser("Script to analyze incoming DNS traffic")
    parser.add_argument("-i", "--interface", default="eth0", help="Interface to use")

    args = parser.parse_args()

    main(args.interface)
