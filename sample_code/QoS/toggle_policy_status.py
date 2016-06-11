#!/usr/bin/env python
from argparse import ArgumentParser
import requests
import json
import os.path, sys
#change path to allow import from parent directory
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
from apic import get_auth_token, create_url, wait_on_task

# get the policy by name
# move all applications to default relevance



def main(apic, user, password, policyid):
    token = get_auth_token(controller_ip=apic, username=user, password=password)

    url = create_url(path="policy", controller_ip=apic)

    print "GET %s" % url
    headers= { 'x-auth-token': token['token']}
    try:
        response = requests.get(url+"/%s" % policyid, headers=headers, verify=False)
    except requests.exceptions.RequestException  as cerror:
        print "Error processing request", cerror
        sys.exit(1)
    policy = response.json()['response']
    print json.dumps(policy, indent=2)
    if policy['state'] == "Active":
        policy['state'] = 'Inactive'
    else:
        policy['state'] = "Active"
    print "Setting policy %s to %s" %(policy['policyName'], policy['state'])
    headers['Content-Type'] = 'application/json'
    policylist = [policy]
    try:
        response = requests.put(url, headers=headers, data=json.dumps(policylist), verify=False)
        print json.dumps(response.json()['response'])
        taskid = response.json()['response']['taskId']
        wait_on_task(taskid, token)
    except requests.exceptions.RequestException  as cerror:
        print "Error processing request", cerror
        sys.exit(1)

if __name__ == "__main__":
    parser = ArgumentParser(description='Select options.')
    # Input parameters
    parser.add_argument('--apic', type=str, required=True,
                        help="The APIC IP or DN")
    parser.add_argument('-u', '--user', type=str, default='admin',
                        help="Go on, guess!")
    parser.add_argument('-p', '--password', type=str, default='cisco',
                        help="Yep, this one too! ;-)")
    parser.add_argument('--policyid', type=str,
                        help="policy ID ;-)")


    args = parser.parse_args()

    main(args.apic, args.user, args.password, args.policyid)