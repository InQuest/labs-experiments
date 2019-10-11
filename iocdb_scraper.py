import requests
import json
from pprint import pprint 

def scrape_iocdb_domains(choice=""):
    '''
    Returns a list of the latest urls available from the InQuest Lab's iocdb tool
    parameters options for choice= "ipaddress", "url", "domain", "hash", or "" for all
    '''
    url = "https://labs.inquest.net/api/iocdb/list"
    response = requests.request("GET", url)
    res = json.loads(response.text)
    results=[]
    for item in res["data"]:
        print(item["artifact_type"], len(item["artifact_type"]))
        if(item["artifact_type"] == choice):
            print("passed")
            results.append(item)
    return results

results = scrape_iocdb_domains(choice="hash");
x=0

for item in results:
    x+=1
    print("{0}/{1}: {2}".format(x,len(results),item["artifact"]))