import requests
import json
from pprint import pprint 

def scrape_repdb_domains():
    '''
    Returns a list of the latest urls available from the InQuest Lab's repdb tool
    '''
    url = "https://labs.inquest.net/api/repdb/list"
    response = requests.request("GET", url)
    res = json.loads(response.text)
    results=[]
    for item in res["data"]:
        results.append(item["data"])
        print(item)
    return results

results = scrape_repdb_domains();
x=0

for item in results:
    x+=1
    print("{0}/{1}: {2}".format(x,len(results),item))