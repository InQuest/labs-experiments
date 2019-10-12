#  This command line tool is for the use of labs.inquest.net in the terminal.
#  The package itself can also be used as a library for your python scripts.
#
# Get your api key here:
#
#  For any questions, contact Adam Musciano (needmorecowbell) at amusciano@inquest.net

import inquestlabs
import os
import argparse

header=None

if __name__ == "__main__":

    labs= inquestlabs.inquestlabs()

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
        labs.set_API_key(args.key)

    if(args.full):
        if(args.verbose): print("Pulling in iocs from iocdb and repdb...")

        for ioc in labs.aggregate_labs_iocs():
            print("Getting hashes associated with ",ioc["ioc"])
            hashes= labs.get_hashes_associated_with_ioc(ioc)
            if(len(hashes)>0):
                fname=ioc["ioc"].replace("/","_")
                try:
                    if(ioc["type"] == "hash"): # if the ioc is a hash itself, don't make a folder
                        labs.download_dfi_artifact_by_hash(ioc["ioc"])
                    else:
                        os.mkdir(fname)
                        for h in hashes:
                            if(args.verbose): print("Hash: ",h)
                            status = labs.download_dfi_artifact_by_hash(h,path=fname)
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
                hashes= labs.get_hashes_associated_with_ioc(ioc)
                if(args.verbose): print("Hashes: ",hashes)
                if(len(hashes)>0):
                    try:
                        if(ioc["type"] == "hash"): # if the ioc is a hash itself, don't make a folder
                            labs.download_dfi_artifact_by_hash(ioc["ioc"])
                        else:
                            os.mkdir(fname)
                            for h in hashes:
                                if(args.verbose): print("Hash: ",h)
                                status = labs.download_dfi_artifact_by_hash(h,path=fname)
                    except Exception as e:
                        pass
    elif(args.hash):
        if(args.verbose): print("Downloading hash: "+args.hash)
        labs.download_dfi_artifact_by_hash(args.hash)
    elif(args.url):
        if(args.verbose): print("Getting associated hashes for: "+args.url)
        res = labs.request_dfi_url(args.url)
        for h in res:
            print(res)
    elif(args.ip):
        if(args.verbose): print("Getting associated hashes for: "+args.ip)
        res = labs.request_dfi_ip(args.ip)
        for h in res:
            print(res)
    elif(args.domain):
        if(args.verbose): print("Getting associated hashes for: "+args.domain)
        res = labs.request_dfi_domain(args.domain)
        for h in res:
            print(res)
    elif(args.embedded):
        if(args.verbose): print("Getting associated hashes for: "+args.embedded)
        res = labs.search_dfi_embedded_logic(args.embedded)
        for h in res:
            print(res)
