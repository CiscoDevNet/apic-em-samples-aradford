#!/usr/bin/env python
from __future__ import print_function
import requests
import sys
import json
import os.path, sys
import csv
#change path to allow import from parent directory
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
from apic import get_auth_token, create_url, wait_on_task
from name_wrapper import name_wrap
from list_projects import get_project_names

def create_project(project_name):
    token = get_auth_token()
    url = create_url(path="pnp-project")

    print ("POST URL %s" % url)
    print ("Creating project %s" % project_name)
    headers= { 'x-auth-token': token['token'], 'content-type' : 'application/json'}
    body = [{"siteName": project_name}]
    try:
        response = requests.post(url, headers=headers, data=json.dumps(body), verify=False)
    except requests.exceptions.RequestException  as cerror:
        print ("Error processing request", cerror)
        sys.exit(1)

    taskid = response.json()['response']['taskId']
    print ("Waiting for Task %s" % taskid)
    task_result = wait_on_task(taskid, token)

    return task_result

if __name__ == "__main__":
    if len(sys.argv) >1  and sys.argv[1] == "-a":
        project_names = get_project_names()

        for project in project_names:
            response = create_project(name_wrap(project))
            print (json.dumps(response, indent=2))
    else:
        response = create_project(name_wrap("Canberra"))
        print (json.dumps(response, indent=2))