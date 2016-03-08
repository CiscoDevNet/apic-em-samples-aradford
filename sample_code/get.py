#!/usr/bin/env python

from apic import get_auth_token, create_url
# get IP address and other base config
from apic_config import APIC, APIC_USER, APIC_PASSWORD
import logging
import sys
import requests
import json
logging.captureWarnings(True)


def get(path):
    url = create_url(path=path)
    print url
    token = get_auth_token()
    headers = {'X-auth-token' : token['token']}
    try:
        response = requests.get(url, headers=headers, verify=False)
    except requests.exceptions.RequestException as cerror:
        print "Error processing request", cerror
        sys.exit(1)

    return response.json()

def main(url):

    if url is None:
        print "usage: url"
        sys.exit(1)

    print "Getting url", url[0]
    response = get(url[0])
    print json.dumps(response['response'],indent=2)


if __name__ == "__main__":
    main(sys.argv[1:])