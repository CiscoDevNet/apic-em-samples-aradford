#!/usr/bin/env python

from login import login
DEVICES=["212.1.10.1"]

def get_ports(apic, deviceId):
    print (deviceId)
    ports = apic.interface.getInterfaceByDeviceId(deviceId=deviceId)
    return [ p  for p in ports.response if p.interfaceType == "Physical"]

def get_port_count(apic, uuid):
    ports = get_ports(apic, uuid)
    up = len([ p for p in ports if p.status == "up"])
    return up, len(ports)

# connect to APIC using the login module
apic = login()

for deviceip in DEVICES:

    network_device = apic.networkdevice.getNetworkDeviceByIp(ipAddress=deviceip)
    active_ports, total_ports = get_port_count(apic, network_device.response.id)
    print('{ip:<16s} {name:<16s} {serial:12s} {active_ports:n} {total_ports:n}'.format(
        ip=network_device.response.managementIpAddress,
        name=network_device.response.hostname,
        serial=network_device.response.serialNumber,
        active_ports=active_ports,
        total_ports=total_ports
    ))