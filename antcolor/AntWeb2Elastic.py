from elasticsearch import Elasticsearch
from elasticsearch import helpers
import requests
import json

#Every run set this to last ant successfully added (last number printed)
lastIn = 37900 #Use to continue after errors and skip bad specimens

querySize = 13000 #Size of the query sent to AntWeb every run
myindex = 'allants4'

offset = lastIn
es = Elasticsearch()
r = requests.get('http://api.antweb.org/v3.1/specimens?hasImage=true&limit=' + str(querySize) + '&offset=' + str(offset))
r = r.json()
specimens = r['specimens']
progress = 0
i = lastIn + 1 #used to add sortingid to specimens. sorting id starts at 1 or the id after the lastIn
for s in specimens:
    s['sortingid'] = i
    es.index(index=myindex, doc_type='_doc', body=s)
    print(i)
    i += 1

