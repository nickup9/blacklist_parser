import requests
import io
import os
import gzip
import re
import csv

# Make a new dir for the blacklist
try:
    os.mkdir('blacklist')
except FileExistsError:
    pass

os.chdir('blacklist')
cwd = os.getcwd()

print('Getting UCEPROTECT Level 2 Blacklist')
# Get level 2.
url = 'http://wget-mirrors.uceprotect.net/rbldnsd-all/dnsbl-2.uceprotect.net.gz'
level_two = requests.get(url)
# Write to file
level_two_filename = cwd + '/uce_level_two.txt'
with open(level_two_filename, 'w') as f:
    f.write(level_two.text)


print('Getting UCEPROTECT Level 3 Blacklist')
# Get level 3
url = 'http://wget-mirrors.uceprotect.net/rbldnsd-all/dnsbl-3.uceprotect.net.gz'
level_three = requests.get(url)
# Write to file
level_three_filename = cwd + '/uce_level_three.txt'
with open(level_three_filename, 'w') as f:
    f.write(level_three.text)

print('Getting spamhaus asndrop list')
# Get spamhaus asndrop.txt
url = 'https://www.spamhaus.org/drop/asndrop.txt'
spamhaus = requests.get(url)
# Write to file
spamhaus_filename = cwd + '/spamhaus_drop.txt'
with open(spamhaus_filename, 'w') as f:
    f.write(spamhaus.text)

# Get MIT results, in CSV form
print('Getting MIT results')
url = 'https://raw.githubusercontent.com/ctestart/BGP-SerialHijackers/master/prediction_set_with_class.csv'
mit = requests.get(url)
# Write to file
mit_filename = cwd + '/mit_results.csv'
with open(mit_filename, 'w') as f:
    f.write(mit.text)



# Now to parse the files
# We have the following objectives:
# 1. Add all ASNs to the list, using some sorta regex
#    For MIT, read the CSV and do things
# 2. Ensure there are no duplicates
# 3. Make sure that the output is neat and in a standardized format of AS#### newline

blacklist_text = cwd + '/blacklist.txt'
with open(blacklist_text, 'w') as blacklist:
    asn_list = []
    # Parse level_two
    with open(level_two_filename, 'r') as f:
        asn_list = asn_list + re.findall(r'AS\d+', f.read())
    # Parse level_three
    with open(level_three_filename, 'r') as f:
        asn_list = asn_list + re.findall(r'AS\d+', f.read())
    # Parse spamhaus
    with open(spamhaus_filename, 'r') as f:
        asn_list = asn_list + re.findall(r'AS\d+', f.read())

    # Parse the MIT
    with open(mit_filename, newline = '') as f:
        mit_reader = csv.DictReader(f, delimiter = ',')
        for row in mit_reader:
            if row['HardVotePred'] == '1':
                asn_list.append('AS' + row['ASN'])

    asn_list = list(dict.fromkeys(asn_list))
    for asn in asn_list:
        blacklist.write(asn + '\n')
