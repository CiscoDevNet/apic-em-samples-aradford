#!/usr/bin/env python

import os, sys
import ast
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from  login import login
from apic_config import APIC, APIC_USER, APIC_PASSWORD
import requests
import json
import re
from argparse import ArgumentParser
from jinja2 import Template
from jinja2 import StrictUndefined

########### This is only need until uniq gets suppport for CLI API
# API ENDPOINTS
ENDPOINT_TICKET = "ticket"
ENDPOINT_TASK_SUMMARY ="task/%s"
RETRY_INTERVAL=2

# -------------------------------------------------------------------
# Helper functions
# -------------------------------------------------------------------
def create_url(path, controller_ip=APIC):
    """ Helper function to create a APIC-EM API endpoint URL
    """

    return "https://%s/api/v1/%s" % (controller_ip, path)


def get_auth_token(controller_ip=APIC, username=APIC_USER, password=APIC_PASSWORD):
    """ Authenticates with controller and returns a token to be used in subsequent API invocations
    """

    login_url = create_url(ENDPOINT_TICKET, controller_ip,)

    data = {
        "username": username,
        "password": password
    }
    headers={"Content-Type" : "application/json"}
    result = requests.post(url=login_url, data=json.dumps(data), headers=headers, verify=False)
    result.raise_for_status()

    token = result.json()["response"]["serviceTicket"]
    return {
        "controller_ip": controller_ip,
        "token": token
    }

class Cmd(object):
    def __init__(self):
        self.token = get_auth_token()
        self.url= create_url(path='network-device-poller/cli/read-request')
    def run(self,  devs, cmds):
        payload = {
                    "name" : "show ver",
                    "deviceUuids" : devs,
                    "commands" : cmds
                    #"commands" : ["show ver | inc IOS"],
                    #"deviceUuids" : [ "068e3625-b413-42b4-a07d-134081c1ff01"]
                }

        try:
            headers = {'x-auth-token': self.token['token'], 'content-type': 'application/json'}
            response = requests.post(self.url, data=json.dumps(payload), headers=headers,verify=False)
        except requests.exceptions.RequestException as cerror:
            print ("Error processing request", cerror)
            return None
        return response.json()

class Response(object):
    def __init__(self, res):
        self.response = res

class Task(object):
    def __init__(self,taskId):
        self.taskId = taskId
##
def atoi(text):
    '''
    helper function for natural sorted list
    :param text:
    :return:
    '''
    return int(text) if text.isdigit() else text

def natural_sort(portlist):
    '''
    sort a list of interfaces.
    :param portlist:
    :return:
    '''
    return sorted(portlist, key=lambda port: [ atoi(c) for c in re.split('(\d+)', port)])

def run_command(apic, ids, cmds):

    c=Cmd()
    if cmds is [None]:
        cmds =["show clock"]
    print (cmds)
    response = c.run(ids, cmds)
    if response:
        #print(response)
        # keep uniq happy
        task=Response(Task(response['response']['taskId']))

        task_response=apic.task_util.wait_for_task_complete(task, timeout=10)
        if task_response:

            # only needed until we fix the output of this progress field to be json
            fileId=ast.literal_eval(task_response.progress)['fileId']

            file = apic.file.downLoadFile(fileId=fileId)

            return file.text

def deviceip_to_id(apic, device_ip):
    network_device = apic.networkdevice.getNetworkDeviceByIp(ipAddress=device_ip)
    return network_device.response.id

def tag_to_ip(apic, tag):
    if tag is None:
        return []

    topology = apic.topology.getPhysicalTopology()

    return [ node.ip for node in topology.response.nodes if node.tags and tag in node.tags]

def deviceid_to_ip(apic, deviceId):
    network_device = apic.networkdevice.getNetworkDeviceById(id=deviceId)
    return network_device.response.managementIpAddress

def match_interfaces(apic, deviceId, regexp):
    ports_response = apic.interface.getInterfaceByDeviceId(deviceId=deviceId)
    ports = apic.serialize(ports_response.response)
    return natural_sort([p['portName'] for p in ports if re.search(regexp, p['portName'])])

def format_response(apic, res_json, human):
    if human:
        for response in res_json:
            success = response['commandResponses']['SUCCESS']
            failure = response['commandResponses']['FAILURE']
            devuuid = response["deviceUuid"]
            for key in success.keys():
                print ('{ip}: {command}:\n{success}\n{failure}'.format(ip=deviceid_to_ip(apic, devuuid),
                                                               command=key, success=success[key],
                                                     failure=failure))
    else:
        print (json.dumps(res_json, indent=2))

if __name__ == "__main__":
    parser = ArgumentParser(description='Select options.')

    parser.add_argument('--commands', type=str,
                        help="commands to run")
    parser.add_argument('--intregexp', type=str,
                        help="interface regular expression (requires a {{INTF}} parameter in the command")
    parser.add_argument('--tag', type=str,
                        help="tag for devices to choose")
    parser.add_argument('--ip', type=str,
                       help="ip address for devices to choose")
    parser.add_argument('--human', action='store_true',
                        help="human output or machine")
    parser.add_argument('-v', action='store_true',
                        help="verbose")
    args = parser.parse_args()
    apic = login()
    print ("tag:", args.tag)
    ips = None
    if args.tag:
        ips = tag_to_ip(apic, args.tag)

    elif args.ip:
        ips = [args.ip]

    if ips:
        ids = [deviceip_to_id(apic, ip) for ip in ips]
    else:
        print ("no ips or tags for network devices")
        exit(1)
    #print ("commands:", args.commands)
    try:
        cmds = json.loads(args.commands)
    except ValueError:
        cmds = [args.commands]

    res = run_command(apic, ids=ids, cmds=cmds)
    res_json = json.loads(res)
    format_response(apic, res_json, args.human)



# max of 5 commands per request