#!/usr/bin/env python

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from login import login

def file_id_lookup(apic):
    file_list = apic.file.getFilesByNamespace(nameSpace="config")
    file_id_dict = {file.id : file.name for file in file_list.response}
    return file_id_dict

def list_all_projects(apic):
    response=""
    file_id_map = file_id_lookup(apic)
    projects = apic.pnpproject.getPnpSiteByRange()
    for project in projects.response:
        print(project.siteName, project.deviceCount)
        if project.deviceCount > 0:
            devices = apic.pnpproject.getPnpSiteDevicesBySiteNameAndRange(projectId=project.id)
            for device in devices.response:
                #filename = apic.file.getFilesByNamespace(nameSpace="config", id=device.configId)
                filename = file_id_map[device.configId] if device.configId in file_id_map else ""
                response += "{0} {1} {2} {3} {4} {5}".format(
                    device.hostName, device.serialNumber, device.platformId,
                    device.configId, filename, device.state)
    return response
if __name__ == "__main__":
    apic = login()
    response = list_all_projects(apic)
    print(response)