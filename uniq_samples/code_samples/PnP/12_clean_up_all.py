#!/usr/bin/env python

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from login import login
from name_wrapper import name_wrap
import csv
from pnp_config import DEVICES


def remove_project(apic, project_name):
    project_name = name_wrap(project_name)
    project = apic.pnpproject.getPnpSiteByRange(siteName=project_name)
    if project.response != []:
        project_id = project.response[0].id
        pnp_task_response = apic.pnpproject.deletePnpSiteByID(projectId=project_id, deleteRule=1, deleteDevice=1)
        task_response = apic.task_util.wait_for_task_complete(pnp_task_response, timeout=5)
        print (apic.serialize(task_response))
    else:
        print ("No project named %s" % project_name)

def is_file_present(apic, namespace, filename):
    filename = name_wrap(filename)
    file_list = apic.file.getFilesByNamespace(nameSpace=namespace)
    fileid_list = [file.id for file in file_list.response if file.name == filename]
    return None if fileid_list == [] else fileid_list[0]

def remove_file(apic, filename):
    # lookupfile by name
    file_id = is_file_present(apic, "config", filename)
    if file_id is None:
        print("file not present: %s"% filename)
        return
    # file deletion is sync
    file_task = apic.file.deleteFile(fileId=file_id)
    print(apic.serialize(file_task))


def clean_up_all(apic, devices):

    f = open(devices, 'rt')
    try:
        reader = csv.DictReader(f)
        for dict_row in reader:
            print (dict_row)

            config_filename = dict_row['hostName'] + '-config'
            remove_project(apic, dict_row['site'])
            remove_file(apic, config_filename)

            print("cleaned site: %s" % name_wrap(dict_row['site']))

    finally:
        f.close()

if __name__ == "__main__":
    apic = login()
    clean_up_all(apic, devices=DEVICES)