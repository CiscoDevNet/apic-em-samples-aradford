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

# if this is true, will not actually call the spark API
#NO_SPARK_API = True
NO_SPARK_API = False

SEEN_CHAT={}
SEEN_PROJECT={}

def check_for_new_project(apic):
    currenttime = time.time()
    projects = apic.pnpproject.getPnpSiteByRange()
    for project in projects.response:
        if project.siteName not in SEEN_PROJECT:
            post_to_spark("APIC>New project created: %s" % project.siteName)
        # update timestamp
        SEEN_PROJECT[project.siteName] = currenttime

    for projectname in list(SEEN_PROJECT):
        if SEEN_PROJECT[projectname] != currenttime:
            print(SEEN_PROJECT[projectname], currenttime, projectname)
            post_to_spark("APIC>Deleted Project: %s" % projectname)
            del SEEN_PROJECT[projectname]


def post_to_spark(message):
    print(message)
    if NO_SPARK_API:
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
        check_for_new_project(apic)
        time.sleep(3)

if __name__ == "__main__":
    main()