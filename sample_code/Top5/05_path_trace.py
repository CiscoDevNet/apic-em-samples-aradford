#!/usr/bin/env python
from __future__ import print_function
import sys
import json
import logging
from argparse import ArgumentParser
from util import get_url, post_and_wait


def create_path_trace(args):
    data = {
        "sourceIP" : args.srcip,
        "destIP" : args.dstip,
        "periodicRefresh" : False
    }
    if  args.srcport is not None:
        data["sourcePort"] =  args.srcport
    if  args.dstport is not None:
        data["destPort"] =  args.dstport

    if args.stats:
        data["inclusions"]  = ["INTERFACE-STATS","DEVICE-STATS"]
    print(json.dumps(data))
    result = post_and_wait("flow-analysis", data)
    return result['progress']

def display_path(pathid):
    path_data = get_url("flow-analysis/%s" % pathid)['response']
    print(json.dumps(path_data,indent=2))
    for network_element in path_data['networkElementsInfo']:
        element_type = None
        if 'type' in network_element:
            element_type = network_element['type']

        if element_type == "wired" or element_type == "wireless":
            print("{ip}:{element_type}".format(ip=network_element["ip"],element_type=element_type))
        else:
            try:
                ingress = network_element["ingressInterface"]["physicalInterface"]["name"]
            except KeyError:
                ingress = None
            try:
                egress = network_element["egressInterface"]["physicalInterface"]["name"]
            except KeyError:
                egress = None

            if ingress is not None:
                print("{ingress_int}".format(ingress_int=ingress))

            try:
                link_info=network_element['linkInformationSource']
            except KeyError:
                link_info=""
            print("{name:>18}:{ip:12} {link_info}".
                  format(name=network_element['name'],
                         ip=network_element['ip'],
                         link_info=link_info))
            if egress is not None:
                print("{egress_int}".format(egress_int=egress))
            print("")

if __name__ == "__main__":
    parser = ArgumentParser(description='Select options.')
    parser.add_argument('--srcip', type=str, required=True,
                        help="src ip address")
    parser.add_argument('--dstip', type=str, required=True,
                        help="dst ip address")
    parser.add_argument('--srcport', type=str,
                        help="source port")
    parser.add_argument('--dstport', type=str,
                        help="dest port")
    parser.add_argument('--stats', action='store_true',
                        help="enable stats collection")

    parser.add_argument('-v', action='store_true',
                        help="verbose")
    args = parser.parse_args()
    if args.v:
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

    pathid  = create_path_trace(args)
    display_path(pathid)