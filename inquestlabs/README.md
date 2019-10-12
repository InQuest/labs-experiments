# Grab associated hashes

This util allows you to get the associated hashes of an ioc. You have the option of adding an api key, this is important if you are trying to do a full scan.

**Usage**

```
dfi_tool.py [-h] [-l LIST] [-f] [--hash HASH] [--url URL] [--ip IP]
                 [--domain DOMAIN] [--embedded EMBEDDED] [-v] [-k KEY]

optional arguments:
  -h, --help            show this help message and exit
  -l LIST, --list LIST  path to file or directory of rules used on list of
                        feeds
  -f, --full            scan full iocdb/repdb list
  --hash HASH           request hash from labs
  --url URL             request hashes associated with url (or partial) from
                        labs
  --ip IP               request hashes associated with an ip from labs
  --domain DOMAIN       request hashes associated with domain (or partial)
                        from labs
  --embedded EMBEDDED   request hashes associated with embedded logic from
                        labs
  -v, --verbose         increase verbosity
  -k KEY, --key KEY     scan full iocdb/repdb list
```

**Examples**

Full Scan
`$ python3 grab_associated_hashes.py -k <key here> -f -v`

Custom Scan
`python3 grab_associated_hashes.py -v -l associated_hash_ioc_list`

Download hash
`python3 grab_associated_hashes.py --hash <hash>`

Download get hashes for domain
`python3 grab_associated_hashes.py --domain <domain>`


**Tips**

Partial searches are available for some of the dfi searches. For example, add the line `/Invoice,url` to your associated_hash_ioc_list file (category options are url, hash, ipaddress, and domain), you will return all associated hashes for that partial url. This is valuable for matching url patterns.