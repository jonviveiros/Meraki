#! python3
# printOrgs.py - Prints a pretty table of associated Meraki orgs.

import meraki
import pprint

print('Enter your API key:')
apikey = input()
print('You entered: ' + apikey)

print('\nmeraki.myorgaccess')
myOrgs = meraki.myorgaccess(apikey)
print(myOrgs)

print('\npprint meraki.myorgaccess')
pprint.pprint(meraki.myorgaccess(apikey))

print('Enter the Org ID:')
orgid = input()
print('You entered: ' + orgid)
#orgid = 756963

print('\nmeraki.mygetnetworklist')
pprint.pprint(meraki.getnetworklist(apikey, orgid))
