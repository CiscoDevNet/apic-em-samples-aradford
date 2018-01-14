#!/usr/bin/env python
from __future__ import print_function
import requests
import csv
import sys
from apic import get_auth_token, create_url


#   ---------------------------------------------------
#   Return info on Network Device based on its ID
#   ---------------------------------------------------
def get_device_info(deviceID):
    url = create_url(path="network-device/" + deviceID)
    token = get_auth_token()
    headers = {'X-auth-token': token['token']}
    try:
        response = requests.get(url, headers=headers, verify=False)
    except requests.exceptions.RequestException as cerror:
        print("Error processing request", cerror)
        sys.exit(1)

    return response.json()


#   ---------------------------------------------------
#   Return all interfaces on all network devices
#   ---------------------------------------------------
def get_interfaces():
    url = create_url(path="interface")
    token = get_auth_token()
    headers = {'X-auth-token' : token['token']}
    try:
        response = requests.get(url, headers=headers, verify=False)
    except requests.exceptions.RequestException as cerror:
        print ("Error processing request", cerror)
        sys.exit(1)

    return response.json()

def print_no_newline(string):
    sys.stdout.write(string)
    sys.stdout.flush()

def main():
    interface_response = get_interfaces()

    # Write new CSV file
    with open('VlanReport.csv', 'w') as csvfile:
        fieldnames = ['Device', 'PID', 'Description', 'Interface', 'VLAN', 'PortStatus']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        # For all interfaces which have a VLAN assigned write this interface in the CSV file
        for interface in interface_response['response']:
            if interface['vlanId'] != u'':
                print_no_newline('*'),
                deviceInfo = get_device_info(interface['deviceId'])

                writer.writerow({'Device': deviceInfo['response']['hostname'],
                                 'PID': interface['pid'],
                                 'Description': interface['description'],
                                 'Interface': interface['portName'],
                                 'VLAN': interface['vlanId'],
                                 'PortStatus':  interface['status']})



if __name__ == "__main__":
    main()
    print('complete')