#!/usr/bin/env python
from __future__ import print_function
import requests
import sys
import json
import os.path, sys
#change path to allow import from parent directory
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
from apic import get_auth_token, create_url
import csv
from pnp_config import DEVICES

def project_name_to_id(project_name):
    token = get_auth_token()
    url = create_url(path="pnp-project")


    headers= { 'x-auth-token': token['token'], 'content-type' : 'application/json'}
    # look for project by name.  need to get the project id
    search_url = url + '?siteName=%s&offset=1&limit=10' %project_name
    print("GET: %s"  % search_url)
    try:
        response = requests.get(search_url, headers=headers, verify=False)
    except requests.exceptions.RequestException  as cerror:
        print("Error processing request", cerror)
        sys.exit(1)

    # check response.json() for values
    # no match
    # multi match
    # single match

    matches = response.json()['response']
    if len(matches) <1:
        raise ValueError('No matches found for %s' % project_name)
    elif len(matches) > 1:
        raise ValueError("multiple matches found for %s" % project_name)
    else:
        project_id = matches[0]['id']
        return project_id

def get_project_names():
    project_name_list = set()
    f = open(DEVICES, 'rt')
    try:
        reader = csv.DictReader(f)
        for dict_row in reader:
            project_name_list.add(dict_row['site'])
    finally:
        f.close()
    return project_name_list

def list_projects():
    token = get_auth_token()

    url = create_url(path="pnp-project")
    print("Getting %s" % url)
    headers= { 'x-auth-token': token['token']}
    try:
        response = requests.get(url, headers=headers, verify=False)
    except requests.exceptions.RequestException  as cerror:
        print("Error processing request", cerror)
        sys.exit(1)
    return response.json()

def list_project_detail(projectname):
    token = get_auth_token()
    project_id = project_name_to_id(projectname)

    url = create_url(path="pnp-project/%s/device" % project_id)
    print("Getting %s" % url)
    headers= { 'x-auth-token': token['token']}
    try:
        response = requests.get(url, headers=headers, verify=False)
    except requests.exceptions.RequestException  as cerror:
        print("Error processing request", cerror)
        sys.exit(1)
    return response.json()


if __name__ == "__main__":

    if len(sys.argv) == 2:
        project_devices = list_project_detail(sys.argv[1])
        for device in project_devices['response']:
            print(json.dumps(device, indent=2))
    else:
        response = list_projects()
        print('{0:16} {1:15} {2:12} {3:32}'.format('siteName','state','deviceCount', 'id'))
        for project in response['response']:
            #print json.dumps(project, indent=2)
            print('{0:16} {1:15} {2:12} {3:32}'.format(project['siteName'], project['state'],
                                                       project['deviceCount'], project['id']))