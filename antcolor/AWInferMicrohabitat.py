from elasticsearch import Elasticsearch

#query specimens from your elasticsearch
es = Elasticsearch()
r = es.search(index='allants6', doc_type='_doc', body={'from': 0, 'size': 50000, 'query': {"exists" : { "field" : "microhabitat"}}})
dictspecimens = r['hits']['hits']

#for every specimen...
progress = 0
for specimen in dictspecimens:
    string = str(specimen['_source']['microhabitat'])

    #CATEGORY 1- underground microhabitat
    if(('in ground' in string) or ('soil' in string)):
        specimen['_source']['microhabitatInferred'] = 'underground'
        print("underground")
    #CATEGORY 2- litter microhabitat
    elif (('litter' in string)):
        specimen['_source']['microhabitatInferred'] = 'litter'
        print("litter")
    #CATEGORY 3- ground foraging
    elif(('ground forager' in string) or ('on ground' in string)):
        specimen['_source']['microhabitatInferred'] = 'ground'
        print("ground")
    #CATEGORY 4- arboreal microhabitat
    elif (('on tree' in string) or ('above ground' in string) or ('in tree' in string) or ('stem' in string) or ('sapling' in string) or ('low vegetation' in string) or  ('beating' in string) or ('trunk' in string and not('fallen' in string))):
        specimen['_source']['microhabitatInferred'] = 'arboreal'
        print("arboreal")

    else:
        specimen['_source']['microhabitatInferred'] = None;

for s in dictspecimens:
    specimen = s['_source']
    id = s['_id']
    es.index(index='allants6', doc_type='_doc', id=id, body=specimen)
    progress += 1
    print(progress)

#low vegetation / above ground
