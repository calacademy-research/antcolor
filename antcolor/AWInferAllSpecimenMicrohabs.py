from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from elasticsearch_dsl import A
import pandas as pd
import colorsys

#Query specimens from your Elasticsearch
es = Elasticsearch()
size = 100000
lastAnalyzed = 400000
#Search to get all species entries
query_body = {
    "sort": [{"sortingid": {"order": "asc"}}, "_score"], 'from': (lastAnalyzed - 1), 'size': size, 'query': {'exists': {'field':'microhabitat'}}
}

s = Search(using=es, index="allantweb", doc_type="properties").update_from_dict(query_body)
body = s.to_dict()
t = s.execute()

#Setup df of microhabs for each specimen to export
column_names = ["SpecimenCode", "Species", "isSoil", "isGround", "isArboreal","MicrohabString","Caste","sortingID"]
df = pd.DataFrame(columns = column_names)

i = 0;
#For every species
for s in t:
    if(i % 1000 == 0):
        print(i)
    i+=1
    isSoil = False;
    isGround = False;
    isArboreal = False;

    #print(s)
    #print(type(s))
    mh = str(s.microhabitat) #Get microhabitat
    #Common tags - under stone, stone, pierres (stones), tronc (trunk), ground nest, rotten log, carton nest
    # CATEGORY 1 - underground microhabitat
    # Terms
    if (('soil core' in mh) or ('ex root' in mh) or ('under stone' in mh) or ('under rock' in mh) or ('banknest' in mh) or
        (('soil' in mh or 'underground' in mh or 'in ground' in mh or 'below ground' in mh or 'under ground' in mh) and (not ('nest') in mh and not('Nest') in mh and not ('Hole') in mh and not ('hole') in mh))):
        isSoil = True
        #print("Soil")
    # CATEGORY 2 - litter microhabitat
    # Terms: litter (any others?)
    if (('litter' in mh)):
        isGround = True
        #print("Litter")
    # CATEGORY 2 - ground microhabitat
    # Terms: ground forager, on ground, ground nest, pitfall
    if (('ground forager' in mh) or ('on ground' in mh) or ('ground nest' in mh) or ('pitfall' in mh) or ('logex' in mh) or ('stumpex' in mh) or ('lognest' in mh)):
        isGround = True
        #print("Ground")
    # CATEGORY 3 - arboreal microhabitat
    # Terms: on tree, ex dead twig, above ground, in tree, stem, live, low veg, beating canopy, carton, trunk NOT (fallen OR dead), arboreal
    if (('on tree ' in mh) or ('ex dead twig' in mh) or ('above ground' in mh) or ('arboreal' in mh) or ('in tree ' in mh) or ('stem' in mh) or ('live' in mh) or ('low veg' in mh) or ('beating' in mh) or ('canopy' in mh) or ('carton' in mh) or (
                  'trunk' in mh and not (('fallen' in mh) or ('dead') in mh))):
        isArboreal = True
        #print("Arboreal"

    code = s.specimenCode
    species = s.antwebTaxonName
    caste = s.caste
    sortingid = s.sortingid
    df = df.append(pd.DataFrame([[code,species,isSoil,isGround,isArboreal,mh,caste,sortingid]], columns=df.columns))

df.to_csv('specimenmicrohabsfinal3.csv')

