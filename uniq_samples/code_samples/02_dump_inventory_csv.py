#!/usr/bin/env python

import requests.exceptions

from uniq.apis.nb.client_manager import NbClientManager
APIC="sandboxapic.cisco.com"
APIC_USER='devnetuser'
APIC_PASSWORD='Cisco123!'

def login():
    """ Login to APIC-EM northbound APIs in shell.
    Returns:
        Client (NbClientManager) which is already logged in.
    """


    try:
        client = NbClientManager(
                server=APIC,
                username=APIC_USER,
                password=APIC_PASSWORD,
                connect=True)
        return client
    except requests.exceptions.HTTPError as exc_info:
        if exc_info.response.status_code == 401:
            print('Authentication Failed. Please provide valid username/password.')
        else:
            print('HTTP Status Code {code}. Reason: {reason}'.format(
                    code=exc_info.response.status_code,
                    reason=exc_info.response.reason))
        exit(1)
    except requests.exceptions.ConnectionError:
        print('Connection aborted. Please check if the host {host} is available.'.format(host=APIC))
        exit(1)


# connect to APIC using the login module
apic = login()

# networkdevice -> NetworkdeviceAPI class.  getAllNetworkDeices is a method in this class
network_devices  = apic.networkdevice.getAllNetworkDevice()

for network_device in apic.serialize(network_devices.response):
    print(",".join(['"{0}"'.format(network_device[k]) for k in network_device.keys()]))
