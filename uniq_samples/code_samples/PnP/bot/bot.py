#!/usr/bin/env python
from spark_config import ROOM, auth

import time
import json
import requests
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from list_all_projects import login, list_all_projects
requests.packages.urllib3.disable_warnings()

url = "https://api.ciscospark.com/v1/messages"

SEEN={}
def parse_and_respond(apic,argv):

    if len(argv) != 2:
        print("Fail")
        return
    if  argv[0] == "show":
        if argv[1] == "pnp-project":
            projects = list_all_projects(apic)
            post_to_spark(projects)
        else:
            post_to_spark("What did you want me to show?")
    else:
        post_to_spark("What did you want me to do?")


def get_spark_command_monitor(apic):

    querystring = {"roomId": ROOM, max : "1"}

    headers = {
    'authorization': auth,
    'content-type': "application/json"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    for item in response.json()['items']:
        if item['id'] not in SEEN:
            SEEN[item['id']] = "Y"
            words = item['text'].split()
            print("GOT:", words[0])
            if words[0] == "APIC":
                parse_and_respond(apic, words[1:])

def post_to_spark(message):
    print(message)
    return
    payload = {"roomId" : ROOM,"text" : message}
    headers = {
    'authorization': auth,
    'content-type': "application/json"
    }
    response = requests.request("POST", url, data=json.dumps(payload), headers=headers)
    print(response.text)


def main():
    apic = login()
    while True:
        get_spark_command_monitor(apic)
        time.sleep(3)

if __name__ == "__main__":
    main()