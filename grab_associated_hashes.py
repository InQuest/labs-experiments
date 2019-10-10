import requests
import json
from pprint import pprint 
import os
import argparse

header=None

def scrape_repdb_domains(key=None):
    '''
    Returns a list of the latest urls available from the InQuest Lab's repdb tool
    '''
    url = "https://labs.inquest.net/api/repdb/list"
    response = requests.request("GET", url, headers=header)
    res = json.loads(response.text)
    results=[]
    for item in res["data"]:
        results.append({"ioc":item["data"] ,"type":"url"})
    return results


def scrape_iocdb_domains(choice="",key=None):
    '''
    Returns a list of the latest urls available from the InQuest Lab's iocdb tool
    parameters options for choice= "ipaddress", "url", "domain", "hash", or "" for all
    '''
    url = "https://labs.inquest.net/api/iocdb/list"
    response = requests.request("GET", url, headers=header)
    res = json.loads(response.text)
    results=[]
    for item in res["data"]:
        if(item["artifact_type"] == choice or choice == ""):
            results.append({"ioc":item["artifact"], "type":item["artifact_type"]})
    return results

def aggregate_labs_iocs():
    results = scrape_iocdb_domains()
    results.extend(scrape_repdb_domains())
    return results

def request_dfi_ip(ip,key=None):
    url = "https://labs.inquest.net/api/dfi/search/ioc/ip?keyword="+ip
    response = requests.request("GET", url, headers=header)
    res= json.loads(response.text)
    results=[]
    for hashObj in res["data"]:
        results.append(hashObj["sha256"])
    return results

def request_dfi_url(url,key=None):
    url = "https://labs.inquest.net/api/dfi/search/ioc/url?keyword="+url
    response = requests.request("GET", url, headers=header)
    res= json.loads(response.text)
    results=[]
    for hashObj in res["data"]:
        results.append(hashObj["sha256"])
    return results

def request_dfi_domain(domain,key=None):
    url = "https://labs.inquest.net/api/dfi/search/ioc/domain?keyword="+domain
    response = requests.request("GET", url,headers=header)
    res= json.loads(response.text)
    results=[]
    for hashObj in res["data"]:
        results.append(hashObj["sha256"])
    return results

def search_dfi_embedded_logic(search,key=None):
    '''
    Searches for a string in the embedded logic of an artifact in the  DFI Database
    Returns a list of hashes
    '''
    url = "https://labs.inquest.net/api/dfi/search/ext/ext_code?keyword="+search
    response = requests.request("GET", url, headers=header)
    res = json.loads(response.text)
    results= []
    for item in res["data"]:
        results.append(item["sha256"])

    return results



def download_dfi_artifact_by_hash(sha, path=""):
    '''
    Given a sha256 hash, this will download the associated file to your current directory
    '''
    url = "https://labs.inquest.net/api/dfi/download?sha256=" + sha
    response = requests.request("GET", url, headers=header)
    if response.status_code == 200:
        if(len(path) > 1):
            with open(path+"/"+sha, "wb+") as fh:
                fh.write(response.content)
        else:
            with open(sha, "wb+") as fh:
                fh.write(response.content)        
    
    return response.status_code

def get_hashes_associated_with_ioc(ioc):
    hashes=[]
    if(ioc["type"] == "url"):
        hashes.extend(request_dfi_url(ioc["ioc"]))
    elif(ioc["type"] == "domain"):
        hashes.extend(request_dfi_domain(ioc["ioc"]))
    elif(ioc["type"] == "ipaddress"):
        hashes.extend(request_dfi_ip(ioc["ioc"]))
    elif(ioc["type"] == "hash"):
        hashes.append(ioc["ioc"])
    print("ioc: "+ioc["ioc"]+"\n\t"+str(hashes))
    return hashes

#pprint(request_dfi_url("seattle.gov"))

if __name__ == "__main__":
 
    parser = argparse.ArgumentParser()
    parser.add_argument("-l","--list", help="path to file or directory of rules used on list of feeds")
    parser.add_argument("-f", "--full", help="scan full iocdb/repdb list", action="store_true")
    parser.add_argument("-v", "--verbose", help="increase verbosity", action="store_true")
    parser.add_argument("-k", "--key", help="scan full iocdb/repdb list")
    args = parser.parse_args()

    if(args.key):
        header= {'Authorization': 'Basic '+args.key}

    if(args.full):
        if(args.verbose): print("Pulling in iocs from iocdb and repdb...")

        for ioc in aggregate_labs_iocs():
            print("Getting hashes associated with ",ioc["ioc"])
            hashes= get_hashes_associated_with_ioc(ioc)
            if(len(hashes)>0):
                fname=ioc["ioc"].replace("/","_")
                try:
                    if(ioc["type"] == "hash"): # if the ioc is a hash itself, don't make a folder
                        download_dfi_artifact_by_hash(ioc["ioc"])
                    else:
                        os.mkdir(fname)
                        for h in hashes:
                            print("Hash: ",h)    
                            status = download_dfi_artifact_by_hash(h,path=fname)
                except Exception as e:
                    print(e)

    else:
        with open(args.list) as f:
            for line in f:
                
                line=line.strip("\n")
                ioc={}
                ioc["ioc"]=line.split(",")[0]
                ioc["type"]=line.split(",")[1]
                fname=ioc["ioc"].replace("/","_")


                print("Getting hashes associated with ",ioc["ioc"])
                hashes= get_hashes_associated_with_ioc(ioc)
                print("Hashes: ",hashes)
                if(len(hashes)>0):
                    try:
                        if(ioc["type"] == "hash"): # if the ioc is a hash itself, don't make a folder
                            download_dfi_artifact_by_hash(ioc["ioc"])
                        else:
                            os.mkdir(fname)
                            for h in hashes:
                                print("Hash: ",h)    
                                status = download_dfi_artifact_by_hash(h,path=fname)          
                    except Exception as e:
                        pass
                  
