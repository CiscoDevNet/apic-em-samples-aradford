from __future__ import print_function

import os
import sys
import requests
import json

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
#from tests.fake import fake, fake_post
#FAKE=True
FAKE=False


from apic import get_auth_token, create_url, wait_on_task

def get_url(url):

    if FAKE:
        return fake[url]
    url = create_url(path=url)
    print(url)
    token = get_auth_token()
    headers = {'X-auth-token' : token['token']}
    try:
        response = requests.get(url, headers=headers, verify=False)
    except requests.exceptions.RequestException as cerror:
        print("Error processing request", cerror)
        sys.exit(1)

    return response.json()

def post_and_wait(url, data):
    if FAKE:
        return fake_post[url]
    token = get_auth_token()
    url = create_url(path=url)
    headers= { 'x-auth-token': token['token'], 'content-type' : 'application/json'}

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data), verify=False)
    except requests.exceptions.RequestException  as cerror:
        print ("Error processing request", cerror)
        sys.exit(1)

    taskid = response.json()['response']['taskId']
    print ("Waiting for Task %s" % taskid)
    task_result = wait_on_task(taskid, token)

    return task_result