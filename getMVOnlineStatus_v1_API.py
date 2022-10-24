#! python3
#
# DEPRECATED - v0 API calls
# DEPRECATED - v0 API calls
# DEPRECATED - v0 API calls

# Created by Victor and J5
# GNU Public license 3.0
#
# rev 1.0 04/23/2021
# last updated 2021-07-22
# Python version: 3.7+
#
# getMVOnlineStatus.py - Walks through a Meraki Organization Devices using Meraki API v1.0 and
#                         creates a list of all Cameras that are online. This list is then written
#                          into an Excel Document.
#
# Dependency requirements: meraki library -  #pip3 install meraki
#                          openpyxl       -  #pip3 install openpyxl
#                          getpass        -  #pip3 install getpass
import openpyxl
from getpass4 import getpass
import meraki


def printListOfOrganizations():
    """ This function prints all Orgs the user has access to and asks the user to choose the Org to interact with """

    orgs = dashboard.organizations.getOrganizations()
    print("\n You have access to {} organizations: \n ".format(len(orgs)))
    print("{} {:<40} {:<20}\n".format("  ", "Org Name:", "Org ID"))
    for i in range(0, len(orgs)):
        print("{}. {:<40} {:<20}".format(i+1, orgs[i]['name'], orgs[i]['id']))
    
    while True:

        choice = int(input("Please select what Org you would like to interact with? (number): "))

        if choice > 0 and choice <= len(orgs):
            print("Preparing -{}- for API interraction...".format(orgs[choice-1]['name']))
            org_id = orgs[choice-1]['id']
            break
        else:
            print("You didn't select a valid choice. Please try again.")

    return org_id


# Main program
if __name__ == '__main__':
    print("you've started...")
    # Get admin's meraki API key to access the dashboard and print all Orgs
    # merakiAPIKey = input('Please enter your Dashboard API Key: ')
    merakiAPIKey = getpass('Please enter your Dashboard API Key: ')
    dashboard = meraki.DashboardAPI(merakiAPIKey)
    OrgID = printListOfOrganizations()

    device_statuses = dashboard.organizations.getOrganizationDevicesStatuses(OrgID, total_pages='all')
    inventory = dashboard.organizations.getOrganizationDevices(OrgID, total_pages='all')
    networks = dashboard.organizations.getOrganizationNetworks(OrgID, total_pages='all')

    i = 1
    output_list = []
    camera_dict = {}

    # Loop through the returned data to identify all camera devices and thier status
    for camera in inventory:
        if camera['model'].startswith('MV'):
            for device in device_statuses:
                # qrprofile = dashboard.camera.getDeviceCameraQualityAndRetention(device['serial'])
                if (device['serial'] == camera['serial']) and device['status'] == 'online':
                    # print('Camera serial is: ' + camera['serial'])
                    # qrprofile = dashboard.camera.getDeviceCameraQualityAndRetention(camera['serial'])
                    for network in networks:
                        if network['id'] == camera['networkId']:
                            network_name = network['name']
                    camera_dict.setdefault('Camera ' + str(i), {'network': network_name,
                                                                'model': camera['model'],
                                                                'name': camera['name'],
                                                                'serial': camera['serial'],
                                                                'status': device['status']
                                                                # ,
                                                                })
                                                                # 'qrprofile': qrprofile['profileId']})
                    output_list.append(camera_dict['Camera ' + str(i)])
                    i += 1

    # Create a workbook that is going to store the MV Status
    mv_workbook = openpyxl.Workbook()
    sheet = mv_workbook.active
    sheet.title = 'MV Status'
    sheet['A1'].value = 'Network'
    sheet['B1'].value = 'Model'
    sheet['C1'].value = 'MV Name'
    sheet['D1'].value = 'Serial'
    sheet['E1'].value = 'Status'
    # sheet['F1'].value = 'QR Profile'

    for index, mv_camera in enumerate(output_list):
        sheet['A' + str(index + 2)].value = mv_camera['network']
        sheet['B' + str(index + 2)].value = mv_camera['model']
        sheet['C' + str(index + 2)].value = mv_camera['name']
        sheet['D' + str(index + 2)].value = mv_camera['serial']
        sheet['E' + str(index + 2)].value = mv_camera['status']
        # sheet['F' + str(index + 2)].value = mv_camera['qrprofile']
    
    # Save the scripts Workbook
    mv_workbook.save('MV_Statuses.xlsx')

    print("Done.")
