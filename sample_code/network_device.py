#!/usr/bin/env python
import requests
import sys
from apic import get_auth_token, create_url


def main():
    url = create_url(path="network-device")
    print url
    token = get_auth_token()
    headers = {'X-auth-token' : token['token']}
    try:
        response = requests.get(url, headers=headers, verify=False)
    except requests.exceptions.RequestException as cerror:
        print "Error processing request", cerror
        sys.exit(1)

    for device in response.json()['response']:
        print device['hostname'], device['managementIpAddress'], \
            device['platformId']

if __name__ == "__main__":
    main()
