#!/usr/bin/env python

from argparse import ArgumentParser
import requests
import json
import os.path, sys
#change path to allow import from parent directory
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
from apic import get_auth_token, create_url, wait_on_task
from apic_config import APIC, APIC_USER, APIC_PASSWORD

# get the policy by name
# move all applications to default relevance

def get_app_from_name(token, app, apic):
    url = create_url(path="application?name=%s" % app, controller_ip=apic)

    print "GET %s" % url
    headers= { 'x-auth-token': token['token']}
    try:
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()
    except requests.exceptions.RequestException  as cerror:
        print "Error processing request", cerror
    return response.json()['response'][0]['id']

def get_relevance(relevance):
    if relevance == "BR":
        return "Business-Relevant"
    elif relevance == "IR":
        return "Business-Irrelevant"
    elif relevance == "D":
        return "Default"
    else:
        print "No mapping for relevance %s" % relevance
        sys.exit(1)

def create_policy(token, apic, policyscope, appname, appid, relevance):

    url = create_url(path="policy", controller_ip=apic)
    policy = [{
        "policyName" : "adam-test",
        "policyScope" : policyscope,
        "policyPriority": 4095,
        "actionProperty" : {
         "pathControlFlag": False,
        "pathPreferenceFlag": False},
        "resource" : {"applications" : [ {"appName": appname, "id" : appid} ]},
        "actionProperty": { "relevanceLevel": relevance },
        "actions" : ["SET_PROPERTY"]
    }]
    headers= { 'x-auth-token': token['token'],
               'content-type' : 'application/json'}
    print "POST", url, json.dumps(policy, indent=2)
    response = requests.post(url, headers=headers, data=json.dumps(policy), verify=False)
    response.raise_for_status()

    task_id = response.json()['response']['taskId']
    task = wait_on_task(task_id, token)
    print json.dumps(task, indent=2)

def main(apic, user, password, policyscope, app, relevance):
    token = get_auth_token(controller_ip=apic, username=user, password=password)

    appid = get_app_from_name(token, app, apic)
    relevancename = get_relevance(relevance)
    #except:
    #    print "Couuld not get app names %s" % app
    #    sys.exit(1)
    print "APP %s" % appid
    create_policy(token, apic, policyscope, app, appid, relevancename)



if __name__ == "__main__":
    parser = ArgumentParser(description='Select options.')
    # Input parameters
    parser.add_argument('--apic', type=str, default=APIC,
                        help="The APIC IP or DN")
    parser.add_argument('-u', '--user', type=str, default=APIC_USER,
                        help="Go on, guess!")
    parser.add_argument('-p', '--password', type=str,default=APIC_PASSWORD,
                        help="Yep, this one too! ;-)")
    parser.add_argument('--policyscope', type=str,
                        help="Policy Scope")
    parser.add_argument('--app', type=str,
                        help="application name")
    parser.add_argument('--relevance', type=str,
                        help="relevance [BR - business-relevant, BI - business-irrelevant, D- default]")

    args = parser.parse_args()

    main(args.apic, args.user, args.password, args.policyscope, args.app, args.relevance)
