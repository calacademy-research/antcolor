from elasticsearch import Elasticsearch

#query specimens from your elasticsearch
es = Elasticsearch()
r = es.search(index='allants2', doc_type='_doc', body={'from': 0, 'size': 30000, 'query': {'match_all': {}}})
# print(r['hits'])
dictspecimens = r['hits']['hits']

#for every specimen...
progress = 0
for specimen in dictspecimens:
    output = ''
    string = specimen['_source']['microhabitat']
    #rock or ground or soil or litter present, tree or above ground not present
    if(' rock ' in string) or (' ground ' in string) or (' soil ' in string) or (' litter ' in string):
        output = 'ground'

    #"tree" or "above ground" present, "stump" not present
    if ((' tree ' in string) or (' above ground ' in string)) and ((' stump ') not in string):
        output = 'tree'
    specimen['_source']['microhabitatInferred'] = output;

for s in dictspecimens:
    specimen = s['_source']
    id = s['_id']
    es.index(index='allants2', doc_type='_doc', id=id, body=specimen)

    #low vegetation / above ground
