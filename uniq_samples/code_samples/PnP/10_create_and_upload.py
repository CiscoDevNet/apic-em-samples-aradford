#!/usr/bin/env python

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from login import login
from name_wrapper import name_wrap
import jinja2
import json
import os.path
import csv

from pnp_config import DEVICES, TEMPLATE, CONFIGS_DIR

def lookup_and_create(apic, project_name):
    project_name = name_wrap(project_name)
    project = apic.pnpproject.getPnpSiteByRange(siteName=project_name)

    if project.response != []:
        project_id = project.response[0].id
    else:
        # create it
        print ("creating project:{project}".format(project=project_name))
        pnp_task_response= apic.pnpproject.createPnpSite(project=[{'siteName' :project_name}])
        task_response = apic.task_util.wait_for_task_complete(pnp_task_response, timeout=5)

        # 'progress': '{"message":"Success creating new site","siteId":"6e059831-b399-4667-b96d-8b184b6bc8ae"}'
        progress = task_response.progress
        project_id = json.loads(progress)['siteId']

    return project_id

# this is due to lack of parameterized search aPI
def is_file_present(apic, namespace, filename):
    filename = filename
    file_list = apic.file.getFilesByNamespace(nameSpace=namespace)
    fileid_list = [file.id for file in file_list.response if file.name == filename]
    return None if fileid_list == [] else fileid_list[0]

# what if file already uploaded?
def upload_file(apic, filename):
    #file_present = apic.file.getFilesByNamespace(nameSpace="config", name=filename)
    #if file_present.response is not []:
    #    print ("File %s already uploaded: %s" % ("2960-client.txt", file_present))
    #    return file_present.response[0].id

    file_id = is_file_present(apic, "config", os.path.basename(filename))
    if file_id is not None:
        print ("File %s already uploaded: %s" %(filename, file_id))
        return file_id

    file_result = apic.file.uploadFile(nameSpace="config", fileUpload=filename)
    file_id = file_result.response.id
    return file_id

def create_rule(apic, param_dict, project_id, file_id):
    serial_number = name_wrap(param_dict['serialNumber'], fixed_len=True)
    rule_data = [{
        "serialNumber": serial_number,
        "platformId":  param_dict['platformId'],
        "hostName": param_dict['hostName'],
        "configId" : file_id,
        "pkiEnabled": True
}]
    print(json.dumps(rule_data,indent=2))
    rule_task = apic.pnpproject.createPnpSiteDevice(projectId=project_id, rule=rule_data)
    task_response = apic.task_util.wait_for_task_complete(rule_task, timeout=5)
    progress = task_response.progress
    print(progress)

def create_and_upload(apic, devices, template_file):
    templateLoader = jinja2.FileSystemLoader( searchpath="." )
    templateEnv = jinja2.Environment( loader=templateLoader )
    template = templateEnv.get_template(template_file)

    f = open(devices, 'rt')
    try:
        reader = csv.DictReader(f)
        for dict_row in reader:
            print (dict_row)
            outputText = template.render(dict_row)
            config_filename = name_wrap(CONFIGS_DIR + dict_row['hostName'] + '-config')
            with open(config_filename, 'w') as config_file:
                config_file.write(outputText)
            project_id = lookup_and_create(apic, dict_row['site'])
            file_id = upload_file(apic, config_filename)
            create_rule (apic, dict_row, project_id, file_id)

            print("created file: %s" % config_filename)

    finally:
        f.close()

if __name__ == "__main__":
    apic = login()
    create_and_upload(apic, devices=DEVICES, template_file=TEMPLATE)