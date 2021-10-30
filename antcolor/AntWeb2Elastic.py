from elasticsearch import Elasticsearch
from elasticsearch import helpers
from elasticsearch import TransportError
import requests
import json
import time

#Every run set this to last ant successfully added (last number printed)
lastIn = 701195 #Use to continue after errors and skip bad specimens
querySize = 10000 #Size of the query sent to AntWeb every run
myindex = 'allantweb'
es = Elasticsearch()

while(lastIn < 770000):
    offset = lastIn
    url = 'https://antweb.org/v3.1/specimens?limit=' + str(querySize) + '&offset=' + str(offset) + '&up=1'
    print(url)
    r = requests.get(url,verify=True)
    r = r.json()
    specimens = r['specimens']
    progress = 0
    i = lastIn + 1 #used to add sortingid to specimens. sorting id starts at 1 or the id after the lastIn
    for s in specimens:
        s['sortingid'] = i
        try:
            es.index(index=myindex, doc_type='_doc', body=s)
        except TransportError:
            print("Parsing exception skipped")
            pass
        #if(i % 1000 == 0):
        print(i)
        i += 1
    lastIn += querySize

