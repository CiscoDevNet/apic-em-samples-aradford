#!/usr/bin/env python
from __future__ import print_function
import sys
from util import get_url
import re
import json

# helper for natural sort
def atoi(text):
    return int(text) if text.isdigit() else text

# natural sort for interfaces
def natural_sort(interfacelist):
    return sorted(interfacelist, key=lambda port: [ atoi(c) for c in re.split('(\d+)', port['portName'])])

def ip_to_id(ip):
    return get_url("network-device/ip-address/%s" % ip)['response']['id']

def get_interfaces(id):
   return get_url("interface/network-device/%s" % id)


def get_hosts(ip):
    return get_url("host?connectedDeviceIp=%s" % ip)

def print_info(interfaces,hosts):
    # this is a hash of the interface_id and hosts that are connected, so can do a lookup
    id_to_host = {host['connectedInterfaceId'] : (host['hostIp'], host['hostMac'])
                    for host in hosts['response'] if host['hostType'] != "wireless"}

    total_up = 0
    total_ports = 0
    print("{0:25}:{1:9} {2:7}{3:10}{4:6} {5}".format("Interface Name","Speed","Status","Type","Vlan","Other"))
    for interface in natural_sort(interfaces['response']):
        if interface['id'] in id_to_host:
            ip, mac = id_to_host[interface['id']]
            extra = "{ip}/{mac}".format(ip=ip,mac=mac)

        elif interface['ipv4Address'] is not None:
            extra = "{ip}/{mask}".format(ip=interface['ipv4Address'], mask=interface['ipv4Mask'])
        elif interface['portMode'] == "trunk":
            extra = "{trunk}{description}".format(trunk=interface['portMode'],description=interface['description'])
        else:
            extra = ""

        if interface['interfaceType'] == "Physical":
            total_ports +=1
            if interface['status'] == "up":
                total_up+=1
        print("{portName:25}:{speed:9} {status:7}{interfaceType:10}{vlanId:6} {extra}".format(portName=interface['portName'],
                                                           speed=interface['speed'],
                                                           status=interface['status'],
                                                            interfaceType=interface['interfaceType'],
                                                            vlanId=interface['vlanId'],
                                                            extra=extra))
        utilization = (total_up * 100) / total_ports
    # now the utilization summary
    print("Utilization:{utilization}%, Total ports:{total_ports}, Total up:{total_up}".
              format(total_ports=total_ports,
                     total_up=total_up,
                     utilization=utilization ))
if __name__ == "__main__":
    if len(sys.argv) > 1:
        dev_id = ip_to_id(sys.argv[1])
        interfaces = get_interfaces(dev_id)
        hosts = get_hosts(sys.argv[1])

        print_info(interfaces, hosts)
    else:
        print("Usage: %s device_ip" % sys.argv[0])