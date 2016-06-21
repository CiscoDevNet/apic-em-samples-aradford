#!/usr/bin/env python
from __future__ import print_function
import requests
import sys
import json
import os.path, sys
import logging
from delete_project import project_name_to_id
import csv

#change path to allow import from parent directory
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
from apic import get_auth_token, create_url, wait_on_task
from name_wrapper import name_wrap
from pnp_config import DEVICES
from list_files import list_files

def create_project_rule(project_name, serial, platform, host, config_file_id=None):
    token = get_auth_token()
    url = create_url(path="pnp-project")
    headers= { 'x-auth-token': token['token'], 'content-type' : 'application/json'}


    project_id = project_name_to_id(project_name)
    post_url = url + '/%s/device' % project_id
    print("POST URL %s" % post_url)

    body = [{
        "serialNumber": serial,
        "platformId": platform,
        "hostName": host,
        "pkiEnabled": True
}]
    if config_file_id is not None:
        body[0]['configId'] = config_file_id

    print(json.dumps(body, indent=2))
    try:
        response = requests.post(post_url, headers=headers, data=json.dumps(body), verify=False)
        response.raise_for_status()

    except requests.exceptions.RequestException  as cerror:
        print("Error processing request", cerror)
        if response.json():
            print(json.dumps(response.json(), indent=2))
        sys.exit(1)

    taskid = response.json()['response']['taskId']
    print("Waiting for Task %s" % taskid)
    task_result = wait_on_task(taskid, token)

    return task_result

if __name__ == "__main__":
    if len(sys.argv) >1  and sys.argv[1] == "-a":
        filelist = list_files('config')['response']
        filetuple = [(file['name'], file['id']) for file in filelist]

        project_name_list = set()
        f = open(DEVICES, 'rt')
        try:
            reader = csv.DictReader(f)
            for dict_row in reader:
                filename = name_wrap(dict_row['hostName'] + "-config")

                fileid = [ id for fn, id in filetuple if fn == filename][0]
                response = create_project_rule(name_wrap(dict_row['site']),
                                               serial=name_wrap(dict_row['serialNumber'], fixed_len=True),
                                               platform=dict_row['platformId'],
                                               host=dict_row['hostName'],
                                               config_file_id=fileid)
                print(json.dumps(response, indent=2))
        finally:
            f.close()

    else:
        response = create_project_rule(name_wrap("Canberra"), serial=name_wrap("12345678910", fixed_len=True ),
                                       platform="2960x", host="device", )
        print(json.dumps(response, indent=2))