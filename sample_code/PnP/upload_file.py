#!/usr/bin/env python

import requests
import sys
import json
import os.path, sys
#change path to allow import from parent directory
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
from apic import get_auth_token, create_url

# this is a sample file to upload.
SAMPLE_FILE = "test_files/config/2960-client.txt"

def upload_file(namespace, filepath):
    token = get_auth_token()

    try:
        f = open(filepath, "r")
        files = {'fileUpload': f}
    except:
        print "Could not open file %s" % filepath
        sys.exit(1)

    url = create_url(path="file/%s" % namespace)

    print "POST %s" % url
    headers= { 'x-auth-token': token['token']}

    try:
        response = requests.post(url, files=files, headers=headers, verify=False)
    except requests.exceptions.RequestException  as cerror:
        print "Error processing request", cerror
        sys.exit(1)
    return response.json()

if __name__ == "__main__":
    response = upload_file("config", SAMPLE_FILE)
    print json.dumps(response['response'], indent=2)