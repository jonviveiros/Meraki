# !/usr/bin/python3
# JViveiros

# DESCRIPTION
# The goal is to pull switchport information from all switches in a Meraki
# network and then export to a .csv file. Use printOrgs.py to get net_id

# USAGE
# python3 exportSwitchportInfo-2.py -k <api_key> -o <org_id> -n <net_id>
# arguments -k and -o are required, argument -n is optional

import csv
from datetime import datetime
import getopt
import sys
import requests
import json

# Prints READ_ME help message for user to read
def print_help():
    print('This python script requires arguments.')
    print('     -h   Help')
    print('     -k   API Key')
    print('     -0   Org ID')
    print('     -n   Net ID (optional)')


# Oops, something bad happened
def print_error():
    print('You made a fatal error.')
    print('Try again.')


def get_inventory(api_key, org_id):
    url = 'https://api.meraki.com/api/v0/organizations/{}/inventory'.format(org_id)
    try:
        response = requests.get(url=url, headers={'X-Cisco-Meraki-API-Key': api_key, 'Content-Type': 'application/json'})
        return json.loads(response.text)
    except requests.exceptions.RequestException as e:
        print('Error calling get_inventory: {}'.format(e))


def get_switchports(api_key, serial):
    url = 'https://api.meraki.com/api/v0/devices/{}/switchPorts'.format(serial)
    try:
        response = requests.get(url=url, headers={'X-Cisco-Meraki-API-Key': api_key, 'Content-Type': 'application/json'})
        return json.loads(response.text)
    except requests.exceptions.RequestException as e:
        print('Error calling get_switchports: {}'.format(e))


def main(argv):
    # Set default values for command line arguments
    api_key = None
    org_id = None
    net_id = None


    # Get command line arguments
    try:
        opts, args = getopt.getopt(argv, 'hk:o:n:')
    except getopt.GetoptError:
        print_help()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print_help()
            sys.exit()
        elif opt == '-k':
            api_key = arg
            print('Your API Key is: '+api_key)
        elif opt == '-o':
            org_id = arg
            print('Your Org ID is: '+org_id)
        elif opt == '-n':
            net_id = arg
            print('Your Net ID is: '+net_id)
    # TODO net_id is optional - may need to be removed in future

    # Check if all required parameters have been input
    if api_key == None or org_id == None:
        print_help()
        sys.exit(2)

    # Set the CSV output file and write the header row
    timenow = '{:%Y%m%d_%H%M%S}'.format(datetime.now())
    filename = 'ms_switchport_config_{0}.csv'.format(timenow)
    output_file = open(filename, mode='w', newline='\n')
    field_names = ['Hostname', 'Serial Number', 'Port', 'Description', 'Mode', 'VLAN', 'VoiceVLAN', 'Allowed VLANS']
    csv_writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    csv_writer.writerow(field_names)
    print('STATUS: Created file: '+str(filename))

    # Find all MS switches and save to a 'switches' dictionary
    session = requests.session()
    inventory = get_inventory(api_key, org_id)
    switches = [device for device in inventory if device['model'][:2] in ('MS') and device['networkId'] is not None]


    # For loop to cycle through each switch
    # ----Creates a list of serial numbers and hostnames
    switch_host_serials = []
    net_count = []
    for switch in switches:
        if switch['serial'] not in switch_host_serials:
            switch_host_serials.append([switch['serial'],switch['name']])

    # ----Creates a list of network IDs; used only for status counter today
        if (switch['networkId']) not in net_count:
            net_count.append(switch['networkId'])

    # Prints out a multi-level lists with serial numbers and hostnames
    print(switch_host_serials)
    # Prints total # of switches in organization
    print('Found a total of %d switches configured across %d networks in this organization.' % (len(switches), len(net_count)))

    i = 0
    # For loop to iterate through each rows in switch_host_serials
    for row in range(len(switch_host_serials)):

        # Prints a quick status counter, serial number and hostname
        print('Count '+str(i+1)+'/'+str(len(switches))+':  Gathering data for '+switch_host_serials[i][1]+' - '+switch_host_serials[i][0])

        # Creates a dictionary of switchport data, csv_row looks for each item's key and places the value
        switchports = get_switchports(api_key, switch_host_serials[row][0])
        for item in switchports:
            csv_row = [switch_host_serials[i][1]], [switch_host_serials[i][0]], item['number'], item['name'], item['type'], item['vlan'], item['voiceVlan'], item['allowedVlans']
            csv_writer.writerow(csv_row)
            #break
        i += 1
        #break


if __name__ == '__main__':
    inputs = sys.argv[1:]
    try:
        key_index = inputs.index ('-k')
    except ValueError:
        print_help()
        sys.exit(2)

    main(sys.argv[1:])
