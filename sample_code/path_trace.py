#!/usr/bin/env python
import requests
import sys
import json
from apic import get_auth_token, create_url, wait_on_task


def path_trace():
    '''

    :return: the result of path trace
    '''
    url = create_url(path="flow-analysis")
    print url
    data = {"sourceIP" : "65.1.1.46", "destIP" : "212.1.10.20"}
    token = get_auth_token()
    headers = {'X-auth-token' : token['token'],
               'Content-Type' : 'application/json'}
    try:
        response = requests.post(url, data=json.dumps(data),
                                 headers=headers, verify=False)
    except requests.exceptions.RequestException as cerror:
        print "Error processing request", cerror
        sys.exit(1)

    taskid = response.json()['response']['taskId']
    print "Waiting for Task %s" % taskid
    task_result = wait_on_task(taskid, token)
    flow_id = task_result['progress']
    url = create_url(path="flow-analysis/%s" % flow_id)
    try:
        response = requests.get(url, headers=headers, verify=False)
    except requests.exceptions.RequestException as cerror:
        print "Error processing request", cerror
        sys.exit(1)

    return response.json()

if __name__ == "__main__":
    path_response = path_trace()
    for node in path_response['response']['networkElementsInfo']:
        print json.dumps(node, indent=2)
