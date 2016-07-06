#!/usr/bin/env python

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from login import login

def list_all_projects(apic):
    projects = apic.pnpproject.getPnpSiteByRange()
    for project in projects.response:
        print(project.siteName, project.deviceCount)
        if project.deviceCount > 0:
            devices = apic.pnpproject.getPnpSiteDevicesBySiteNameAndRange(projectId=project.id)
            for device in devices.response:
                filename = apic.file.getFilesByNamespace(nameSpace="config", id=device.configId)

                print (device.hostName, device.serialNumber, device.platformId, device.configId, filename.response[0].name, device.state)

if __name__ == "__main__":
    apic = login()
    list_all_projects(apic)