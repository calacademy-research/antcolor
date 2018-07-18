from elasticsearch import Elasticsearch
from elasticsearch import helpers
import requests
import json

es = Elasticsearch()
r = requests.get('http://api.antweb.org/v3.1/specimens?hasImage=true&limit=15000&offset=36899')
r = r.json()
specimens = r['specimens']
progress = 0
for s in specimens:
    es.index(index='allants3', doc_type='_doc', body=s)
    progress+=1
    print(progress)

