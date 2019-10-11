# Grab associated hashes

This util allows you to get the associated hashes of an ioc. You have the option of adding an api key, this is important if you are trying to do a full scan.

**Usage**

```
python3 grab_associated_hashes.py -h
usage: grab_associated_hashes.py [-h] [-l LIST] [-f] [-v] [-k KEY]

optional arguments:
  -h, --help            show this help message and exit
  -l LIST, --list LIST  path to file or directory of rules used on list of
                        feeds
  -f, --full            scan full iocdb/repdb list
  -v, --verbose         increase verbosity
  -k KEY, --key KEY     scan full iocdb/repdb list

```

**Examples**

Full Scan
`$ python3 grab_associated_hashes.py -k <key here> -f -v`

Custom Scan
`python3 grab_associated_hashes.py -v -l associated_hash_ioc_list`


**Tips**

Partial searches are available for some of the dfi searches. For example, add the line `/Invoice,url` to your associated_hash_ioc_list file (category options are url, hash, ipaddress, and domain), you will return all associated hashes for that partial url. This is valuable for matching url patterns.