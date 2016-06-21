#!/usr/bin/env python

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from  login import login

apic = login()
projects = apic.pnpproject.getPnpSiteByRange()

print('{id:^36s} {name:^12s}'.format(id='Project ID', name='SiteName'))
for project in projects.response:
    print('{id:<36s} {name:<12s}'.format(id=project.id, name=project.siteName))