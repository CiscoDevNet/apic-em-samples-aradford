from login import login

# connect to APIC using the login module
apic = login()

# networkdevice -> NetworkdeviceAPI class.  getAllNetworkDeices is a method in this class
network_devices  = apic.networkdevice.getAllNetworkDevice()

# print a heading
print('{ip:<16s} {name:<16s}'.format(ip="IP Address", name="Device Name"))

# print each of the nework devices.  network_devices is a list of objects with attributes, not a python dict
for network_device in network_devices.response:
    print('{ip:<16s} {name:<16s}'.format(ip=network_device.managementIpAddress, name=network_device.hostname))