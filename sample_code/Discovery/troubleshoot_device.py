#!/usr/bin/env python
from __future__ import print_function
import requests
import sys
import json
import os.path, sys
#change path to allow import from parent directory
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
from apic import get_auth_token, create_url

def troubleshoot(deviceip):
    token = get_auth_token()

    print('Reachability test for device:%s' % deviceip)

    url = create_url(path="reachability-info/ip-address/%s" % deviceip)
    print("Getting %s" % url)
    headers= { 'x-auth-token': token['token']}
    try:
        response = requests.get(url, headers=headers, verify=False)
    except requests.exceptions.RequestException  as cerror:
        print("Error processing request", cerror)
        sys.exit(1)

    print(json.dumps(response.json(), indent=2))
    dev = response.json()['response']
    print('Status: {status}'.format(status=dev['reachabilityStatus']))
    if 'reachabilityFailureReason' in dev:
        print(dev['reachabilityFailureReason'])

    url = create_url(path="network-device/management-info")
    print("Getting %s" % url)
    headers= { 'x-auth-token': token['token']}
    try:
        response = requests.get(url, headers=headers, verify=False)
    except requests.exceptions.RequestException  as cerror:
        print("Error processing request", cerror)
        sys.exit(1)
    print(json.dumps(response.json(), indent=2))
    for cred in response.json()['response']:
        if cred['managementIpAddress'] == deviceip:
            print(json.dumps(cred, indent=2))

if __name__ == "__main__":
    troubleshoot(sys.argv[1])