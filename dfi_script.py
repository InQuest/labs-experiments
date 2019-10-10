import requests
import json
from pprint import pprint 

def search_dfi_embedded_logic(search):
    '''
    Searches for a string in the embedded logic of an artifact in the  DFI Database
    Returns a list of hashes
    '''
    url = "https://labs.inquest.net/api/dfi/search/ext/ext_code?keyword="+search
    response = requests.request("GET", url)
    res = json.loads(response.text)
    results= []
    for item in res["data"]:
        results.append(item["sha256"])

    return results

def download_dfi_artifact_by_hash(sha):
    '''
    Given a sha256 hash, this will download the associated file to your current directory
    '''
    url = "https://labs.inquest.net/api/dfi/download?sha256=" + sha
    response = requests.request("GET", url)
    print(response.status_code)
    if response.status_code == 200:
        with open(sha, "wb+") as fh:
            fh.write(response.content)

hashes= search_dfi_embedded_logic("powershell -executionpolicy bypass")

for sha in hashes:
    download_dfi_artifact_by_hash(sha)