#!/usr/bin/env python

from argparse import ArgumentParser
import requests
import json
import os.path, sys
#change path to allow import from parent directory
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
from apic import get_auth_token, create_url

# get the policy by name
# move all applications to default relevance



def main(apic, user, password, policyscope):
    token = get_auth_token(controller_ip=apic, username=user, password=password)

    url = create_url(path="policy?policyScope=%s" % policyscope, controller_ip=apic)

    print "GET %s" % url
    headers= { 'x-auth-token': token['token']}
    try:
        response = requests.get(url, headers=headers, verify=False)
    except requests.exceptions.RequestException  as cerror:
        print "Error processing request", cerror
        sys.exit(1)
    for policy in response.json()['response']:
        print policy['policyName']
        # look for the business relevant apps
        if '-BR' in policy['policyName']:
            brapps = policy['resource']['applications']
            print "Business Relevant app count: %d" % len(brapps)
        # look for the current default apps
        elif '-D' in policy['policyName']:
            defapps = policy['resource']['applications']
            print "Default app count: %d" % len(defapps)

    apps = brapps + defapps
    print "Total Default app count: %d" % len(apps)
    print

if __name__ == "__main__":
    parser = ArgumentParser(description='Select options.')
    # Input parameters
    parser.add_argument('--apic', type=str, required=True,
                        help="The APIC IP or DN")
    parser.add_argument('-u', '--user', type=str, default='admin',
                        help="Go on, guess!")
    parser.add_argument('-p', '--password', type=str, default='cisco',
                        help="Yep, this one too! ;-)")
    parser.add_argument('--policyscope', type=str,
                        help="Policy Scope")

    args = parser.parse_args()

    main(args.apic, args.user, args.password, args.policyscope)
