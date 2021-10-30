from elasticsearch import Elasticsearch
import requests
import json
import random

####################
#### AWGetRandomImages prints 50 random image links based on the filter for viewing and testing purposes
################

es = Elasticsearch()
r = es.search(index='allants', doc_type='_doc',
              body={"sort": [{"lightness": {"order": "desc"}}, "_score"], 'size': 50000, 'query': {'match_all': {}}})
dictspecimens = r['hits']['hits']
print(type(dictspecimens))
random.shuffle(dictspecimens)

# for every specimen...
for specimen in dictspecimens:
    if(True): #Filters for ants
        c = specimen['_source']['specimenCode']
        print('https://www.antweb.org/v3.1/images?shotType=H&specimenCode=' + c + "&up=1")

        # r = requests.get(
        #     'http://api.antweb.org/v3.1/images?shotType=H&specimenCode=' + c + "&up=1")  # + "&up=1" # adjust shotType as preferred
        # print(r.content)
        # d = r.json()
        #
        # # parse for the new image query
        # p = d['images']
        # #print(p)
        # j = json.dumps(p)
        #
        # # make sure the query has images
        # if (len(j) > 4):
        #     # get first link, which will be the "low quality" image
        #     startindex = j.find('ht')#startindex = j.find('ht')
        #     endindex = j.find('high.jpg')
        #     string = j[startindex:endindex + 8]
        #
        #     print(string)  # prints image link
        #     print(c)  # prints specimen code