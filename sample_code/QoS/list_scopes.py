#!/usr/bin/env python
from argparse import ArgumentParser
import requests
import json
import os.path, sys
#change path to allow import from parent directory
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
from apic import get_auth_token, create_url
from apic_config import APIC, APIC_USER, APIC_PASSWORD

# get the policy by name
# move all applications to default relevance



def main(apic, user, password):
    token = get_auth_token()

    url = create_url(path="policy/tag/association", controller_ip=apic)

    print "GET %s" % url
    headers= { 'x-auth-token': token['token']}
    try:
        response = requests.get(url, headers=headers, verify=False)
    except requests.exceptions.RequestException  as cerror:
        print "Error processing request", cerror
        sys.exit(1)

    for association in response.json()['response']:
        print "Tag:", association['policyTag']
        print "Devices:",
        for network_device in association['networkDevices']:
            print ",", network_device['deviceName'],
        print
        print

if __name__ == "__main__":
    parser = ArgumentParser(description='Select options.')
    # Input parameters
    parser.add_argument('--apic', type=str, default=APIC,
                        help="The APIC IP or DN")
    parser.add_argument('-u', '--user', type=str, default=APIC_USER,
                        help="Go on, guess!")
    parser.add_argument('-p', '--password', type=str,default=APIC_PASSWORD,
                        help="Yep, this one too! ;-)")


    args = parser.parse_args()

    main(args.apic, args.user, args.password)