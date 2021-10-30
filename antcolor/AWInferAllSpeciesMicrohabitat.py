from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from elasticsearch_dsl import A
import pandas as pd

####################
#### AWInferAllSpeciesMicrohabitat leverages Elasticsearch to aggregate all 800k AntWeb specimens into species, counting the number of specimens found in each microhabitat using their collection notes strings
################

#Query specimens from your Elasticsearch
es = Elasticsearch()

#Search to get all species entries
query_body = {
    "size": 800000,
    "aggs": {
        "by_species": {
            "terms": {
                "field": "antwebTaxonName",
                "size": 30000
            }
        }
    }
}
s = Search(using=es, index="allantweb", doc_type="properties").update_from_dict(query_body)
body = s.to_dict()
t = s.execute()

#Aggregate to species
speciesList = [];
for item in t.aggregations.by_species.buckets:
    speciesList.append(item.key)

#Setup df of microhabs for each species to export
column_names = ["Species", "numSoil", "numLitter", "numGround", "numArboreal"]
df = pd.DataFrame(columns = column_names)
#Setup df of uncategorized species to export, used to find new search strings
column_names = ["Species", "mhstring"]
dfUncat = pd.DataFrame(columns = column_names)

i = 0;
#For every species
for species in speciesList:
    print(species)
    print(i)
    i+=1
    query_body = {
        "_source": ["microhabitat"],
        "size": 20000,
        "query": {
            "term": {
                "antwebTaxonName": {
                    "value": species
                }
            }
        }
    }
    s = Search(using=es, index="allantweb", doc_type="properties").update_from_dict(query_body)
    body = s.to_dict()
    t = s.execute()
    numSoil = 0;
    numLitter = 0;
    numGround = 0;
    numArboreal = 0;


    for hit in t: #For every specimen in species
        mh = str(hit.microhabitat) #Get microhabitat
        #Common tags - under stone, stone, pierres (stones), tronc (trunk), ground nest, rotten log, carton nest
        # CATEGORY 1 - underground microhabitat
        # Terms: soil core, underground OR in ground OR below ground OR under ground NOT nest
        if (('soil core' in mh) or
            (('underground' in mh or 'in ground' in mh or 'below ground' in mh or 'under ground' in mh) and (not ('nest') in mh and not('Nest') in mh and not ('Hole') in mh and not ('hole') in mh))):
            numSoil += 1;
            #print('Soil')
        # CATEGORY 2 - litter microhabitat
        # Terms: litter (any others?)
        elif (('litter' in mh)):
            numLitter += 1;
            #print("Litter")
        # CATEGORY 2 - ground microhabitat
        # Terms: ground forager, on ground, ground nest, pitfall
        elif (('ground forager' in mh) or ('on ground' in mh) or ('ground nest' in mh) or ('pitfall' in mh)):
            numGround += 1;
            #print("Ground")
        # CATEGORY 3 - arboreal microhabitat
        # Terms: on tree, ex dead twig, above ground, in tree, stem, live, low veg, beating canopy, carton, trunk NOT (fallen OR dead), arboreal
        elif (('on tree ' in mh) or ('ex dead twig' in mh) or ('above ground' in mh) or ('arboreal' in mh) or ('in tree ' in mh) or ('stem' in mh) or ('live' in mh) or ('low veg' in mh) or ('beating' in mh) or ('canopy' in mh) or ('carton' in mh) or (
                      'trunk' in mh and not (('fallen' in mh) or ('dead') in mh))):
            numArboreal += 1;
            #print("Arboreal")
        #No category, add to uncat for export
        else:
            dfUncat = dfUncat.append(pd.DataFrame([[species,mh]], columns=dfUncat.columns))

    df = df.append(pd.DataFrame([[species,numSoil,numLitter,numGround,numArboreal]], columns=df.columns))

df.to_csv('speciesmicrohabs.csv')
dfUncat.to_csv('microhabUncat.csv')

