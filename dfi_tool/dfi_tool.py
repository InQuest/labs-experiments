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
    '''
    Request the list of iocs from both labs and repdb, then merge the lists together
    Returns a list of dictionaries
    '''
    results = scrape_iocdb_domains()
    results.extend(scrape_repdb_domains())
    return results

def request_dfi_ip(ip,key=None):
    '''
    Request the associated hashes tied to an ip address
    Returns list of hash strings
    '''
    url = "https://labs.inquest.net/api/dfi/search/ioc/ip?keyword="+ip
    response = requests.request("GET", url, headers=header)
    res= json.loads(response.text)
    results=[]
    for hashObj in res["data"]:
        results.append(hashObj["sha256"])
    return results

def request_dfi_url(url,key=None):
    '''
    Request the associated hashes tied to a url
    Returns list of hash strings
    '''
    url = "https://labs.inquest.net/api/dfi/search/ioc/url?keyword="+url
    response = requests.request("GET", url, headers=header)
    res= json.loads(response.text)
    results=[]
    for hashObj in res["data"]:
        results.append(hashObj["sha256"])
    return results

def request_dfi_domain(domain,key=None):
    '''
    Request the associated hashes tied to a domain
    Returns list of hash strings
    '''
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
    '''
    This function routes each ioc dictionary object to it's appropriate handler, which returns the associated hashes.
    Returns list of hash strings
    '''
    hashes=[]
    if(ioc["type"] == "url"):
        hashes.extend(request_dfi_url(ioc["ioc"]))
    elif(ioc["type"] == "domain"):
        hashes.extend(request_dfi_domain(ioc["ioc"]))
    elif(ioc["type"] == "ipaddress"):
        hashes.extend(request_dfi_ip(ioc["ioc"]))
    elif(ioc["type"] == "hash"):
        hashes.append(ioc["ioc"])
    return hashes

if __name__ == "__main__":
 
    parser = argparse.ArgumentParser()
    parser.add_argument("-l","--list", help="path to file or directory of rules used on list of feeds")
    
    parser.add_argument("-f", "--full", help="scan full iocdb/repdb list", action="store_true")
    parser.add_argument("--hash", help="request hash from labs")
    parser.add_argument("--url", help="request hashes associated with url (or partial) from labs")
    parser.add_argument("--ip", help="request hashes associated with an ip from labs")
    parser.add_argument("--domain", help="request hashes associated with domain (or partial) from labs")
    parser.add_argument("--embedded", help="request hashes associated with embedded logic from labs")
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
                            if(args.verbose): print("Hash: ",h)    
                            status = download_dfi_artifact_by_hash(h,path=fname)
                except Exception as e:
                    if(args.verbose): print(e)

    elif (args.list):
        with open(args.list) as f:
            for line in f:
                line=line.strip("\n")
                ioc={}
                ioc["ioc"]=line.split(",")[0]
                ioc["type"]=line.split(",")[1]
                fname=ioc["ioc"].replace("/","_")


                print("Getting hashes associated with ",ioc["ioc"])
                hashes= get_hashes_associated_with_ioc(ioc)
                if(args.verbose): print("Hashes: ",hashes)
                if(len(hashes)>0):
                    try:
                        if(ioc["type"] == "hash"): # if the ioc is a hash itself, don't make a folder
                            download_dfi_artifact_by_hash(ioc["ioc"])
                        else:
                            os.mkdir(fname)
                            for h in hashes:
                                if(args.verbose): print("Hash: ",h)    
                                status = download_dfi_artifact_by_hash(h,path=fname)          
                    except Exception as e:
                        pass
    elif(args.hash):
        if(args.verbose): print("Downloading hash: "+args.hash)
        download_dfi_artifact_by_hash(args.hash)
    elif(args.url):
        if(args.verbose): print("Getting associated hashes for: "+args.url)
        res = request_dfi_url(args.url)
        for h in res:
            print(res)
    elif(args.ip):
        if(args.verbose): print("Getting associated hashes for: "+args.ip)
        res = request_dfi_ip(args.ip)
        for h in res:
            print(res)
    elif(args.domain):
        if(args.verbose): print("Getting associated hashes for: "+args.domain)
        res = request_dfi_domain(args.domain)
        for h in res:
            print(res)
    elif(args.embedded):
        if(args.verbose): print("Getting associated hashes for: "+args.embedded)
        res = search_dfi_embedded_logic(args.embedded)
        for h in res:
            print(res)