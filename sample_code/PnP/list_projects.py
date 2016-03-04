#!/usr/bin/env python

import requests
import sys
import json
import os.path, sys
#change path to allow import from parent directory
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
from apic import get_auth_token, create_url

def list_projects():
    token = get_auth_token()

    url = create_url(path="pnp-project")
    print "Getting %s" % url
    headers= { 'x-auth-token': token['token']}
    try:
        response = requests.get(url, headers=headers, verify=False)
    except requests.exceptions.RequestException  as cerror:
        print "Error processing request", cerror
        sys.exit(1)
    return response.json()
if __name__ == "__main__":
    response = list_projects()
    print '{0:16} {1:15} {2:12} {3:32}'.format('siteName','state','deviceCount', 'id')
    for project in response['response']:
        #print json.dumps(project, indent=2)
        print '{0:16} {1:15} {2:12} {3:32}'.format(project['siteName'], project['state'], project['deviceCount'], project['id'])