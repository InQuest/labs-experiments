import requests
import json
import os

class inquestlabs(object):
    header=None
    def set_API_key(self,key):
        '''
        Sets the api key.
        '''
        self.header= {'Authorization': 'Basic '+key}


    def scrape_repdb_domains(self, key=None):
        '''
        Returns a list of the latest urls available from the InQuest Lab's repdb tool
        '''
        url = "https://labs.inquest.net/api/repdb/list"
        response = requests.request("GET", url, headers=self.header)
        res = json.loads(response.text)
        results=[]
        for item in res["data"]:
            results.append({"ioc":item["data"] ,"type":"url"})
        return results


    def scrape_iocdb_domains(self, choice="",key=None):
        '''
        Returns a list of the latest urls available from the InQuest Lab's iocdb tool
        parameters options for choice= "ipaddress", "url", "domain", "hash", or "" for all
        '''
        url = "https://labs.inquest.net/api/iocdb/list"
        response = requests.request("GET", url, headers=self.header)
        res = json.loads(response.text)
        results=[]
        for item in res["data"]:
            if(item["artifact_type"] == choice or choice == ""):
                results.append({"ioc":item["artifact"], "type":item["artifact_type"]})
        return results

    def aggregate_labs_iocs(self):
        '''
        Request the list of iocs from both labs and repdb, then merge the lists together
        Returns a list of dictionaries
        '''
        results = scrape_iocdb_domains()
        results.extend(scrape_repdb_domains())
        return results

    def request_dfi_ip(self, ip,key=None):
        '''
        Request the associated hashes tied to an ip address
        Returns list of hash strings
        '''
        url = "https://labs.inquest.net/api/dfi/search/ioc/ip?keyword="+ip
        response = requests.request("GET", url, headers=self.header)
        res= json.loads(response.text)
        results=[]
        for hashObj in res["data"]:
            results.append(hashObj["sha256"])
        return results

    def request_dfi_url(self, url,key=None):
        '''
        Request the associated hashes tied to a url
        Returns list of hash strings
        '''
        url = "https://labs.inquest.net/api/dfi/search/ioc/url?keyword="+url
        response = requests.request("GET", url, headers=self.header)
        res= json.loads(response.text)
        results=[]
        for hashObj in res["data"]:
            results.append(hashObj["sha256"])
        return results

    def request_dfi_domain(self, domain,key=None):
        '''
        Request the associated hashes tied to a domain
        Returns list of hash strings
        '''
        url = "https://labs.inquest.net/api/dfi/search/ioc/domain?keyword="+domain
        response = requests.request("GET", url,headers=self.header)
        res= json.loads(response.text)
        results=[]
        for hashObj in res["data"]:
            results.append(hashObj["sha256"])
        return results

    def search_dfi_embedded_logic(self, search,key=None):
        '''
        Searches for a string in the embedded logic of an artifact in the  DFI Database
        Returns a list of hashes
        '''
        url = "https://labs.inquest.net/api/dfi/search/ext/ext_code?keyword="+search
        response = requests.request("GET", url, headers=self.header)
        res = json.loads(response.text)
        results= []
        for item in res["data"]:
            results.append(item["sha256"])

        return results



    def download_dfi_artifact_by_hash(self, sha, path=""):
        '''
        Given a sha256 hash, this will download the associated file to your current directory
        '''
        url = "https://labs.inquest.net/api/dfi/download?sha256=" + sha
        response = requests.request("GET", url, headers=self.header)
        if response.status_code == 200:
            if(len(path) > 1):
                with open(path+"/"+sha, "wb+") as fh:
                    fh.write(response.content)
            else:
                with open(sha, "wb+") as fh:
                    fh.write(response.content)

        return response.status_code

    def get_hashes_associated_with_ioc(self,ioc):
        '''
        This function routes each ioc dictionary object to it's appropriate handler, which returns the associated hashes.
        Returns list of hash strings
        '''
        hashes=[]
        if(ioc["type"] == "url"):
            hashes.extend(self.request_dfi_url(ioc["ioc"]))
        elif(ioc["type"] == "domain"):
            hashes.extend(self.request_dfi_domain(ioc["ioc"]))
        elif(ioc["type"] == "ipaddress"):
            hashes.extend(self.request_dfi_ip(ioc["ioc"]))
        elif(ioc["type"] == "hash"):
            hashes.append(ioc["ioc"])
        return hashes
