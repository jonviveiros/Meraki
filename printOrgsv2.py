#! python3
# Meraki API v1
# Script takes in API Key and responds with Org and Network IDs based on selections

import meraki
from datetime import datetime
from getpass import getpass
# import openpyxl, csv

# timenow = '{:%Y%m%d_%H%M%S}'.format(datetime.now())


def printlistoforganizations():
    """ This function prints all Orgs the user has access to and asks the user to choose the Org to interact with """

    orgs = dashboard.organizations.getOrganizations()
    print("\n You have access to {} organizations: \n ".format(len(orgs)))
    print("{} {:<40} {:<20}\n".format("  ", "Org Name:", "Org ID"))
    for i in range(0, len(orgs)):
        print("{}. {:<40} {:<20}".format(i + 1, orgs[i]['name'], orgs[i]['id']))

    while True:
        choice = int(input("Please select what Org you would like to interact with (number): "))

        if 0 < choice <= len(orgs):
            print("Preparing ---{}--- for API interraction...".format(orgs[choice - 1]['name']))
            org_id_1 = orgs[choice - 1]['id']
            break
        else:
            print("You didn't select a valid choice. Please try again.")
    return org_id_1


def printlistofnetworks():
    global org_id
    nets = dashboard.organizations.getOrganizationNetworks(org_id)
    print("\n You have access to {} networks:".format(len(nets)))
    print("{} {:<40} {:<20}".format("  ", "Network Name:", "Network ID:"))
    for i in range(0, len(nets)):
        print("{}. {:<40} {:<20}".format(i + 1, nets[i]['name'], nets[i]['id']))

    # while True:
    #     choice = int(input("Please select what Network you would like to interact with (number): "))
#
    #     if 0 < choice <= len(nets):
    #         print("Preparing ---{}--- for API interaction...".format(nets[choice - 1]['name']))
    #         net = nets[choice - 1]
    #         return net
    #     else:
    #         print("You didn't select a valid choice. Please try again.")


if __name__ == '__main__':
    # Get API Key
    apikey = getpass(prompt='Enter your API Key: ')
    dashboard = meraki.DashboardAPI(apikey, suppress_logging=True)

    # Chose the org to leverage
    org_id = printlistoforganizations()

    # Chose the network to leverage
    net_info = printlistofnetworks()
    # print('ID #: ' + net_info['id'] + ' AND Network name: ' + net_info['name'])
