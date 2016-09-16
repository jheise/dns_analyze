#!/usr/bin/env python

import argparse
import datastream.analyzer
import geoip2.database

class DomainAnalyzer(datastream.analyzer.Analyzer):
    def __init__(self, zmq_host, zmq_topic, port, database):
        super(DomainAnalyzer, self).__init__(zmq_host, zmq_topic, port)
        self.database = geoip2.database.Reader(database)

    def _analyze(self, data):
        # check if this is a query for a new domain
        try:
            if data["Answers"]:
                for answer in data["Answers"]:
                    if not "query_geolocation" in data:
                        response = self.database.city(answer)
                        geolocation = "{0},{1}".format(response.location.latitude, response.location.longitude)
                        data["query_geolocation"] = geolocation
                        data["query_country"] = response.country.name
                        data["query_city"] = response.city.name
        except Exception as e:
            print e
            #pass

        return data

def main(zmq_host, zmq_topic, port, database):

    domainanalyzer = DomainAnalyzer(zmq_host, zmq_topic, port, database)
    domainanalyzer.activate()
    running = True

    try:
        while running:
            domainanalyzer.process()
    except KeyboardInterrupt:
        running = False

if __name__ == "__main__":

    parser = argparse.ArgumentParser("Script to analyze incoming DNS traffic")
    parser.add_argument("-zh", "--zmq-host", default="tcp://localhost:7777", help="host running zmq dns stream, default tcp://localhost:7777")
    parser.add_argument("-zt", "--zmq-topic", default="dns", help="zmq topic to listen for")
    parser.add_argument("-p", "--port", default=9999, type=int,
        help="port to bind, default 9999")
    parser.add_argument("-d", "--database", default="GeoLite2-Country.mmdb", help="path to geoip database")

    args = parser.parse_args()

    main(args.zmq_host, args.zmq_topic, args.port, args.database)
