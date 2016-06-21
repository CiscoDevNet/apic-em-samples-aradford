#!/usr/bin/env python
from __future__ import print_function
import requests
import sys
from apic import get_auth_token, create_url


def main():
    url = create_url(path="interface")
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
    interface_response = main()
    for interface in interface_response['response']:
        if interface['ipv4Address']:
            print ('{0:16}/{1:16} {2:20}'.\
                format(interface['ipv4Address'],
                       interface['ipv4Mask'],
                       interface['portName']))
