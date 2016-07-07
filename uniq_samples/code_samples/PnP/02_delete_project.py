#!/usr/bin/env python

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from  login import login
from name_wrapper import name_wrap

# create a unique name.  Only required in a lab environment
siteName = name_wrap("adam")
apic = login()

# get the project
pnp_project = apic.pnpproject.getPnpSiteByRange(siteName=siteName)
print (apic.serialize(pnp_project))

try:
    pnp_project_id = pnp_project.response[0].id

    # delete it
    pnp_delete_task_response= apic.pnpproject.deletePnpSiteByID(projectId=pnp_project_id)
    pnp_delete_response = apic.task_util.wait_for_task_complete(pnp_delete_task_response, timeout=5)
    print ("delete", apic.serialize(pnp_delete_task_response))

    print("status", apic.task_util.is_task_success(pnp_delete_task_response))
except ValueError :
    print(e)
