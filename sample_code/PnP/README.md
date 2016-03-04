Some examples for PnP (Plug and Play)
=====================================

Shows how to upload/list/delete config files.  Same approach applies to image files.  
You would just need to change the namespace from "config" to "image"


'''
$ ./list_files.py 
Getting https://sandboxapic.cisco.com:9443/api/v1/file/namespace/config
name                          :fileFormat      fileSize   id                              
ams01-rtr01.txt               :text/plain      530        90a0e4df-93fe-4a7f-884e-0b5b7d8a08d7

'''

There is also an example of listing of projects

'''
$ ./list_projects.py 
Getting https://sandboxapic.cisco.com:9443/api/v1/pnp-project
siteName         state           deviceCount  id                              
JOep             PRE_PROVISIONED            2 3dadbcd2-1ba6-4d4b-8653-3a1f18e2fb25
JoshProject      PRE_PROVISIONED            0 71b20a6f-b841-48db-8b60-0e0c8d2cbc1f
test123          PRE_PROVISIONED            0 2b51a87c-0964-4589-96b8-fbeb5fdc3000
'''