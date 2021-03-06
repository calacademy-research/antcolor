from elasticsearch import Elasticsearch
import requests
import json

es = Elasticsearch()
r = es.search(index='allants', doc_type='_doc',
              body={"sort": [{"lightness": {"order": "desc"}}, "_score"], 'size': 50000, 'query': {'match_all': {}}})
dictspecimens = r['hits']['hits']

# for every specimen...
for specimen in dictspecimens:
    if(specimen['_source']['genus'] == 'Iridomyrmex'):
        c = specimen['_source']['specimenCode']
        r = requests.get(
            'http://api.antweb.org/v3.1/images?shotType=H&specimenCode=' + c)  # adjust shotType as preferred
        d = r.json()

        # parse for the new image query
        p = d['images']
        j = json.dumps(p)

        lightness = 0
        red = 0
        green = 0
        blue = 0
        saturation = 0

        # make sure the query has images
        if (len(j) > 4):
            # get first link, which will be the "low quality" image
            startindex = j.find('ht')
            endindex = j.find('.jp')
            string = j[startindex:endindex + 4]
            print(string)  # prints image link
