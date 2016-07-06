#!/usr/bin/env python
from __future__ import print_function
import sys
from argparse import ArgumentParser
from util import get_url
import json
import logging

def get_host(ip=None, mac=None):
    if ip is not None:
        url = "host?hostIp=%s" % ip
    elif mac is not None:
        url = "host?hostMac=%s" % mac
    return get_url(url)

def get_wlc(id):
    return get_url("network-device/%s" % id)

def print_host(host):
    #print(json.dumps(host, indent=2))

    if 'pointOfPresence' in host:
        wlc = get_wlc(host['pointOfPresence'])['response']
        connection = "-> {hostname} {ip} {platform}({software}) ->  {ap} vlan:{vlan}".\
            format(hostname=wlc['hostname'],
                   ip=wlc['managementIpAddress'],
                   platform=wlc['platformId'],
                   software=wlc['softwareVersion'],
                   ap=host['connectedAPName'],
                   vlan=host['vlanId'])
    else:
        connection = "-> {dev}|{interface} vlan:{vlan}".\
            format(dev=host['connectedNetworkDeviceIpAddress'],
                   interface=host['connectedInterfaceName'],
                   vlan=host['vlanId'])

    print("{ip}|{mac} {type} {connection}".
          format(ip=host['hostIp'],
                 mac=host['hostMac'],
                 type=host['hostType'],
                 connection=connection))

if __name__ == "__main__":
    parser = ArgumentParser(description='Select options.')
    parser.add_argument('--ip', type=str,
                        help="ip address")
    parser.add_argument('--mac', type=str,
                        help="mac address")
    parser.add_argument('-v', action='store_true',
                        help="verbose")
    args = parser.parse_args()
    if args.v:
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


    host = get_host(ip=args.ip, mac=args.mac)
    print_host(host['response'][0])