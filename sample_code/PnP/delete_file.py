#!/usr/bin/env python
import requests
import json
import os.path, sys
#change path to allow import from parent directory
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
from apic import get_auth_token, create_url


def delete_file(namespace, fileid):
    token = get_auth_token()

    url = create_url(path="file/%s" % fileid)

    print "DELETE %s" % url
    headers= { 'x-auth-token': token['token']}

    try:
        response = requests.delete(url,  headers=headers, verify=False)
    except requests.exceptions.RequestException  as cerror:
        print "Error processing request", cerror
        sys.exit(1)
    return response.json()

if __name__ == "__main__":
    if not sys.argv[1]:
        print "No fileID provided"
        sys.exit(1)
    response = delete_file("config", sys.argv[1])
    print json.dumps(response['response'], indent=2)