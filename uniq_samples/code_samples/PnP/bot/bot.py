#!/usr/bin/env python
from spark_config import ROOM, auth

import time
import json
import requests
requests.packages.urllib3.disable_warnings()

url = "https://api.ciscospark.com/v1/messages"

SEEN={}
def parse_and_respond(argv):
    print argv
    #show pnp project


def get_spark_command_monitor():

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
            print "GOT:", words[0]
            if words[0] == "APIC":
                parse_and_respond(words[1:])

def post_to_spark(message):
    payload = {"roomId" : ROOM,"text" : message}
    headers = {
    'authorization': auth,
    'content-type': "application/json"
    }
    response = requests.request("POST", url, data=json.dumps(payload), headers=headers)
    print(response.text)


def main():
    while True:
        get_spark_command_monitor()
        time.sleep(3)

if __name__ == "__main__":
    main()