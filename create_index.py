#!/usr/bin/env python

import elasticsearch
import json

es = elasticsearch.Elasticsearch("10.0.42.4")
es.indices.delete(index="dns-queries")

mapping = { "query": {
                "properties": {
                    "query": {
                        "type": "string",
                        "index": "not_analyzed"},
                    "src_ip": {
                        "type": "string",
                        "index": "not_analyzed"},
                    "timestamp": { "type":"date"}
                }
            }
            }
mappings = { "mappings": mapping }
es.indices.create(index="dns-queries", body=mappings)
