#!/usr/bin/env python
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

    for interface in response.json()['response']:
        if interface['ipv4Address']:

            print interface['ipv4Address'], interface['ipv4Mask'], \
                interface['portName']

if __name__ == "__main__":
    main()
