# blacklist_parser
Quick and dirty parser of blacklisted ASNs from various sources, outputting a directory with the raw data pulled from the sources an a list of ASNs in blacklist.txt

Specifically, it pulls from:
- Spamhaus at https://www.spamhaus.org/drop/asndrop.txt
- UCEPROTECT at http://wget-mirrors.uceprotect.net/rbldnsd-all/dnsbl-2.uceprotect.net.gz and http://wget-mirrors.uceprotect.net/rbldnsd-all/dnsbl-3.uceprotect.net.gz for levels 2 and 3 respectively
- The results of the prediction set based on a BGP Hijacker classifier described in the paper 'Profiling BGP Serial Hijackers: Capturing PersistentMisbehavior in the Global Routing Table' at https://people.csail.mit.edu/ctestart/publications/BGPserialHijackers.pdf from https://raw.githubusercontent.com/ctestart/BGP-SerialHijackers/master/prediction_set_with_class.csv

Simply run in bash using:
```
python3 blacklist_parser.py
```
and the script will create a directory "blacklist" with the raw output from the four sources and a blacklist with the combined ASNs identified as malicious and/or serial hijackers.
