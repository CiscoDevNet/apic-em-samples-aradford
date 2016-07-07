#!/usr/bin/env python
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from  login import login
from name_wrapper import name_wrap

apic = login()

siteName = name_wrap('adam')
pnp_task_response= apic.pnpproject.createPnpSite(project=[{'siteName' :siteName}])
task_response = apic.task_util.wait_for_task_complete(pnp_task_response, timeout=5)
print (apic.serialize(task_response))

print(apic.task_util.is_task_success(pnp_task_response))