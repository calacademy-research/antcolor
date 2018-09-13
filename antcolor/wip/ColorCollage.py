from elasticsearch import Elasticsearch
import requests
import json

#needs hue value, WIP
es = Elasticsearch()
r = es.search(index='allants', doc_type='_doc',
              body={"sort": [{"lightness": {"order": "desc"}}, "_score"], 'size': 50000, 'query': {'match_all': {}}})
dictspecimens = r['hits']['hits']

# for every hue interval of 5
for x in range(0,360):
    if(x == 0 or x % 5 == 0):
        brightest = [(float, str)]
        for specimen in dictspecimens:
            s = specimen['_source']
            #if(s['hue'] = )

