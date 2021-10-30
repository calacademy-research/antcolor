from elasticsearch import Elasticsearch
import requests
from requests.adapters import HTTPAdapter
from requests.adapters import Retry
import json
from io import BytesIO
import colorsys
from PIL import Image
import numpy as np
from timeit import default_timer as timer
import imghdr
import math
import random
from Helpers import CQColorDefs
from Helpers import CQSegmentations
import time
import pandas as pd

lastAnalyzed = 24000
#Start at 1 for first run. Set to last analyzed for subsequent runs
size = 50000

#query specimens from your elasticsearch ordered by
es = Elasticsearch()
r = es.search(index='allantshsv', doc_type='_doc', body={"sort": [{"sortingid": {"order": "asc"}}, "_score"], 'from': lastAnalyzed - 1, 'size': size, 'query': {'match_all': {}}}) #20000-25000 missing?
specimenlist = r['hits']['hits']

#Setup df of microhabs for each specimen to export
column_names = ["specimenCode", "dateImageUploaded"]
df = pd.DataFrame(columns = column_names)

i = 0
for specimen in specimenlist:
    #get specimenCode
    c = specimen['_source']['specimenCode']

    #query date uploaded from AntWeb
    session = requests.Session()
    retry = requests.adapters.Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    url = 'https://antweb.org/v3.1/images?specimenCode=' + c + '&up=1'
    r = requests.get(url)

    # convert image to json
    d = r.json()
    try:
        p = d['images'][0]['images'][0]['uploadDate']
    except KeyError as e:
        print('I got a KeyError: ' + json.dumps(d))
    j = json.dumps(p)
    datevars = j.split(" ")
    if(datevars[0] == "" or datevars[0] == 'null'):
        continue
    day = datevars[1]
    monthname = datevars[2]
    monthnum = time.strptime(monthname, "%b").tm_mon
    year = datevars[3]
    fulldate = str(year) + '/' + str(monthnum) + '/' + str(day)
    df = df.append(pd.DataFrame([[c, fulldate]], columns=df.columns))
    #print(c)
    i += 1
    if (i % 1000 == 0):
        print(i)
        df.to_csv('DateImageUploaded3.csv')

df.to_csv('DateImageUploaded3.csv')