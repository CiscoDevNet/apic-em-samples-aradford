#!/usr/bin/env python
import requests
import sys
from apic import get_auth_token, create_url


def list_network_devices():
    url = create_url(path="network-device")
    print url
    token = get_auth_token()
    headers = {'X-auth-token' : token['token']}
    try:
        response = requests.get(url, headers=headers, verify=False)
    except requests.exceptions.RequestException as cerror:
        print "Error processing request", cerror
        sys.exit(1)

    return response.json()

if __name__ == "__main__":
    response = list_network_devices()
    for device in response['response']:
        print "{0:30} {1:16} {2:15}".format(device['hostname'], device['managementIpAddress'], \
            device['platformId'])
