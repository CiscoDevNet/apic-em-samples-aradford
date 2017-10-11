from flask import Flask, render_template, request
from login import login
import re

app = Flask(__name__)
apic = login()
fake_data=[({'serialNumber' : "wwww", 'id': '223423', 'familty' : 'switch',
             'managementIpAddress' : '1.1.1.1', 'hostname' : 'fred',
             'platformId' : '3850', 'softwareVersion': '16.6.6'}, 10, 20, 30,""),
        ({'serialNumber' : "xxxx", 'id': '223423', 'familty' : 'switch',
             'managementIpAddress' : '1.1.2.1', 'hostname' : 'bill',
             'platformId' : '3850', 'softwareVersion': '16.6.6'}, 12, 10, 32,"")
           ]

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
    return sorted(portlist, key=lambda port: [ atoi(c) for c in re.split('(\d+)', port['portName'])])

def get_license(deviceId):
    # this needs to be fixed
    licenses = apic.license.getLicenseInfo(deviceId=deviceId)
    license_list = [l for l in licenses.response
                    if l.status == "INUSE" or
                    l.status == 'USAGECOUNTCONSUMED']
    return license_list

def get_ports(uuid):
    ports_response = apic.interface.getInterfaceByDeviceId(deviceId=uuid)
    ports = apic.serialize(ports_response.response)
    return natural_sort([ p  for p in ports if p['interfaceType'] == "Physical"])

def get_port_count(uuid):
    ports = get_ports(uuid)
    up = len([ p for p in ports if p['status'] == "up"])
    return up, len(ports)

def get_all_devices():
    device_response = apic.networkdevice.getAllNetworkDevice()
    device_data = apic.serialize(device_response.response)
    for device in device_data:
        if device['family'] == "Unified AP":
            continue
        device['license_list'] = apic.serialize(get_license(device['id']))
        print(device['license_list'])

    return device_data

def get_hosts(ip):
    #return get_request("host?connectedDeviceIp=%s" % ip)
    return get_request("host?connectedNetworkDeviceIpAddress=%s" % ip)
    hosts = apic.connected()
    hostmap[host['connectedInterfaceId']].append("%s->%s" % (host['hostMac'], host['hostIp']))

@app.route('/')
def index():
    device_data = get_all_devices()
    return render_template("index.html", device_data = device_data)

fake_interface=[{'status' : "up", 'portName' : 'gig1/0/1', 'mode': 'access', 'speed' : '10000'}]

@app.route('/device-detail')
def device_detail():
    device_id = request.args.get("device_id", 'None')
    device_ip = request.args.get("device_ip", 'None')
    ports = get_ports(device_id)
    return render_template("interfaces.html", ports = ports, hosts=[], device_ip=device_ip)


if __name__ == '__main__':

    app.run(debug=True)


