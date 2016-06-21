#!/usr/bin/env python
from __future__ import print_function
import requests
import json
import os.path, sys
#change path to allow import from parent directory
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
from apic import get_auth_token, create_url
from pnp_config import CONFIGS_DIR
from list_files import list_files


def delete_file(namespace, fileid):
    token = get_auth_token()

    url = create_url(path="file/%s" % fileid)

    print("DELETE %s" % url)
    headers= { 'x-auth-token': token['token']}

    try:
        response = requests.delete(url,  headers=headers, verify=False)
    except requests.exceptions.RequestException  as cerror:
        print("Error processing request", cerror)
        sys.exit(1)
    return response.json()

if __name__ == "__main__":
    if len(sys.argv) >1  and sys.argv[1] == "-a":
        filelist = list_files('config')['response']
        filetuple = [(file['name'], file['id']) for file in filelist]

        for filename in os.listdir(CONFIGS_DIR):
            if  not filename.startswith('.'):
                print("deleting %s" %filename)
                try:
                    fileid = [ id for fn, id in filetuple if fn == filename][0]
                except IndexError as e:
                    print("file %s not present" % filename)
                else:
                    response = delete_file("config", fileid)
                    print(json.dumps(response['response'], indent=2))
    else:
        response = delete_file("config", sys.argv[1])
        print(json.dumps(response['response'], indent=2))