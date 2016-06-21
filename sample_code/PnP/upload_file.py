#!/usr/bin/env python
from __future__ import print_function
import requests
import sys
import json
import os.path, sys
#change path to allow import from parent directory
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
from apic import get_auth_token, create_url
from name_wrapper import name_wrap
from pnp_config import CONFIGS_DIR

# this is a sample file to upload.
SAMPLE_FILE = "work_files/config/2960-client.txt"

def upload_file(namespace, filepath):
    token = get_auth_token()

    try:
        f = open(filepath, "r")
        files = {'fileUpload': f}
    except:
        print("Could not open file %s" % filepath)
        sys.exit(1)

    url = create_url(path="file/%s" % namespace)

    print("POST %s" % url)
    headers= { 'x-auth-token': token['token']}

    try:
        response = requests.post(url, files=files, headers=headers, verify=False)
    except requests.exceptions.RequestException  as cerror:
        print("Error processing request", cerror)
        sys.exit(1)
    return response.json()

if __name__ == "__main__":
    if len(sys.argv) >1  and sys.argv[1] == "-a":
        for filename in os.listdir(CONFIGS_DIR):
            file = "%s/%s" % (CONFIGS_DIR, filename)
            if os.path.isfile(file) and  not filename.startswith('.'):
                response = upload_file("config", file)
                print(json.dumps(response['response'], indent=2))
    else:
        response = upload_file("config", SAMPLE_FILE)
        print(json.dumps(response['response'], indent=2))