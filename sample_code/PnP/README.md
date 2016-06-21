Some examples for PnP (Plug and Play)
=====================================

Shows how to upload/list/delete config files.  Same approach applies to image files.  
You would just need to change the namespace from "config" to "image"


```
$ ./list_files.py 
Getting https://sandboxapic.cisco.com:9443/api/v1/file/namespace/config
name                          :fileFormat      fileSize   id                              
ams01-rtr01.txt               :text/plain      530        90a0e4df-93fe-4a7f-884e-0b5b7d8a08d7
```


There is also an example of listing of projects

```
$ ./list_projects.py 
Getting https://sandboxapic.cisco.com:9443/api/v1/pnp-project
siteName         state           deviceCount  id                              
JOep             PRE_PROVISIONED            2 3dadbcd2-1ba6-4d4b-8653-3a1f18e2fb25
JoshProject      PRE_PROVISIONED            0 71b20a6f-b841-48db-8b60-0e0c8d2cbc1f
test123          PRE_PROVISIONED            0 2b51a87c-0964-4589-96b8-fbeb5fdc3000
```

# Config Template Automation
The scripts in this directory can be used to automate the deployment of PnP configurations.  Note this is sample code,
designed for educational purposes.  It exposes most of the mechanics under the covers and covers each of the four steps 
in isolation to aid the learning process.

A number of the resources (filename, projectname, serialnumber) need to be unique on APIC-EM.  To allow multiple people to
use this lab with the sandbox controller, a function called "name_wrap" is used to append a 4 digit number to filename and project names.
This suffix is stored in the suffix.py file.  NOTE: Serial numbers need to be 11 digits, so name_wrap just replaces the last 4 digits of the
serial number.

## Build Templates
First step it to build configuration templates.  There are two files used here:  
- [work_files/templates/config_template.jnj](work_files/templates/config_template.jnj) is a jinja2 template file.
- [work_files/inventory.csv](work_files/inventory.csv) is a csv file with an entry for each network device.

The template is very simple, and just illustrates the use of variables.  These variables correspond to the column names of the csv file. In
this case "hostname" and "ipAddress" are two variables that come from the inventory file.
```
hostname {{hostName|lower}}

enable password cisco123
!
username cisco password 0 cisco123
no aaa new-model

int vlan 1
ip address {{ipAddress}}

!
end
```

The inventory file just contains entries for each netork device along with the variables to be instanciated.  You need to provide
"serialNumber", "platformId" and "site" for PnP rules.
```
hostName,serialNumber,platformId,site,ipAddress
sw01,12345678901,WS-C2960X-48FPD-L,Sydney,10.10.10.101
sw02,22345678901,WS-C2960X-48FPD-L,Sydney,10.10.10.102
sw03,32345678901,WS-C2960X-48FPD-L,Melbourne,10.10.10.103
```

to create the configuration files, run the "build_templates.py" command.
``` bash
$ ./build_templates.py 
{'platformId': 'WS-C2960X-48FPD-L', 'hostName': 'sw01', 'ipAddress': '10.10.10.101', 'site': 'Sydney', 'serialNumber': '12345678901'}
wrote file: work_files/configs/sw01-config-6130
{'platformId': 'WS-C2960X-48FPD-L', 'hostName': 'sw02', 'ipAddress': '10.10.10.102', 'site': 'Sydney', 'serialNumber': '22345678901'}
wrote file: work_files/configs/sw02-config-6130
{'platformId': 'WS-C2960X-48FPD-L', 'hostName': 'sw03', 'ipAddress': '10.10.10.103', 'site': 'Melbourne', 'serialNumber': '32345678901'}
wrote file: work_files/configs/sw03-config-6130
```

The output of these files is in the [work_files/configs](work_files/configs) directory.  There will be three files created. 
"6130" is the suffix that was created for me.

## Upload File

Once the config files have been create, they need to be uploaded to the controller.  "upload_file.py -a" will do this.
``` bash
$ ./upload_file.py -a
POST https://sandboxapic.cisco.com/api/v1/file/config
{
  "downloadPath": "/file/a6f40b82-433e-48ac-b5af-c5650148f663", 
  "name": "sw01-config-6130", 
  "sha1Checksum": "7262d0f18380878b1b71898aff364c57cdb9e5fe", 
  "nameSpace": "config", 
  "id": "a6f40b82-433e-48ac-b5af-c5650148f663", 
  "fileSize": "136", 
  "fileFormat": "text/plain", 
  "md5Checksum": "d5d193eaeaa6d7a928215b6068d6d6dc"
}
POST https://sandboxapic.cisco.com/api/v1/file/config
{
  "downloadPath": "/file/99ff9c54-38f8-436f-89e6-8d15bc6fe926", 
  "name": "sw02-config-6130", 
  "sha1Checksum": "656aee9f5fe7b0c6d70e97a8821eb1c01e6ea92f", 
  "nameSpace": "config", 
  "id": "99ff9c54-38f8-436f-89e6-8d15bc6fe926", 
  "fileSize": "136", 
  "fileFormat": "text/plain", 
  "md5Checksum": "e69890b5a6c6089d4bceae786e03c2ce"
}
POST https://sandboxapic.cisco.com/api/v1/file/config
{
  "downloadPath": "/file/e928ee52-81f2-44bc-9a90-c759602c23f1", 
  "name": "sw03-config-6130", 
  "sha1Checksum": "63ea1eb2ff210290a5718c90ca7deb946f97c8bd", 
  "nameSpace": "config", 
  "id": "e928ee52-81f2-44bc-9a90-c759602c23f1", 
  "fileSize": "136", 
  "fileFormat": "text/plain", 
  "md5Checksum": "45295dff681e114a611f3162d813428b"
}

```

Notice that file operations are synchronous, i.e. the operation returns straight away.  Each file has a 32character UUID associated with it.
All other POST commands will be asynchronous.

You can use "list_files.py" to take a look at the files created.

## Create Projects
The next step is to create projects for the rules.  The "create_project.py -a" command does this.
``` bash
$ ./create_project.py -a
POST URL https://sandboxapic.cisco.com/api/v1/pnp-project
Creating project Melbourne-6130
Waiting for Task 27e4dda0-dc46-4d94-89aa-0e53dba81006
{
  "rootId": "27e4dda0-dc46-4d94-89aa-0e53dba81006", 
  "serviceType": "Ztd Service", 
  "id": "27e4dda0-dc46-4d94-89aa-0e53dba81006", 
  "version": 1466501686726, 
  "startTime": 1466501686726, 
  "progress": "{\"message\":\"Success creating new site\",\"siteId\":\"a375afc3-a46c-48aa-a612-3598f465435d\"}", 
  "endTime": 1466501686738, 
  "isError": false
}
POST URL https://sandboxapic.cisco.com/api/v1/pnp-project
Creating project Sydney-6130
Waiting for Task bbc2b13f-b0ac-4ef1-94b5-d348ab107d34
{
  "rootId": "bbc2b13f-b0ac-4ef1-94b5-d348ab107d34", 
  "serviceType": "Ztd Service", 
  "id": "bbc2b13f-b0ac-4ef1-94b5-d348ab107d34", 
  "version": 1466501689258, 
  "startTime": 1466501689258, 
  "progress": "{\"message\":\"Success creating new site\",\"siteId\":\"fbc3338d-9bba-47e8-8905-b5130aa5af9a\"}", 
  "endTime": 1466501689276, 
  "isError": false
}

```
The project creation calls are asynchronous, meaning that a task_id is returned and I need to poll the task_id to determine
if the creation was successful.

## Create Rules
I now create rules for the devices.  This will associate the configuration file created in step #1, uploaded in Step #2, in a rule
 defined in the project created in step #3.  "create_rule.py -a" will create the rules on APIC-EM.

``` bash
$ ./create_rule.py -a
Getting https://sandboxapic.cisco.com/api/v1/file/namespace/config
GET: https://sandboxapic.cisco.com/api/v1/pnp-project?siteName=Sydney-6130&offset=1&limit=10
POST URL https://sandboxapic.cisco.com/api/v1/pnp-project/fbc3338d-9bba-47e8-8905-b5130aa5af9a/device
[
  {
    "platformId": "WS-C2960X-48FPD-L", 
    "hostName": "sw01", 
    "serialNumber": "12345676130", 
    "configId": "a6f40b82-433e-48ac-b5af-c5650148f663", 
    "pkiEnabled": true
  }
]
Waiting for Task 44c59536-fd1e-40f5-bf46-60211949aae2
{
  "rootId": "44c59536-fd1e-40f5-bf46-60211949aae2", 
  "serviceType": "Ztd Service", 
  "id": "44c59536-fd1e-40f5-bf46-60211949aae2", 
  "version": 1466501935290, 
  "startTime": 1466501935290, 
  "progress": "{\"message\":\"Success creating new site device(rule)\",\"ruleId\":\"382f3be4-5632-41d1-9853-4a46561b0b73\"}", 
  "endTime": 1466501935334, 
  "isError": false
}
GET: https://sandboxapic.cisco.com/api/v1/pnp-project?siteName=Sydney-6130&offset=1&limit=10
POST URL https://sandboxapic.cisco.com/api/v1/pnp-project/fbc3338d-9bba-47e8-8905-b5130aa5af9a/device
[
  {
    "platformId": "WS-C2960X-48FPD-L", 
    "hostName": "sw02", 
    "serialNumber": "22345676130", 
    "configId": "99ff9c54-38f8-436f-89e6-8d15bc6fe926", 
    "pkiEnabled": true
  }
]
Waiting for Task 6aa40814-086b-4798-b6b4-45ed41427f8a
{
  "rootId": "6aa40814-086b-4798-b6b4-45ed41427f8a", 
  "serviceType": "Ztd Service", 
  "id": "6aa40814-086b-4798-b6b4-45ed41427f8a", 
  "version": 1466501939737, 
  "startTime": 1466501939737, 
  "progress": "{\"message\":\"Success creating new site device(rule)\",\"ruleId\":\"afe93afe-9dc2-42a3-9a29-f505ec4eb2ba\"}", 
  "endTime": 1466501939785, 
  "isError": false
}
GET: https://sandboxapic.cisco.com/api/v1/pnp-project?siteName=Melbourne-6130&offset=1&limit=10
POST URL https://sandboxapic.cisco.com/api/v1/pnp-project/a375afc3-a46c-48aa-a612-3598f465435d/device
[
  {
    "platformId": "WS-C2960X-48FPD-L", 
    "hostName": "sw03", 
    "serialNumber": "32345676130", 
    "configId": "e928ee52-81f2-44bc-9a90-c759602c23f1", 
    "pkiEnabled": true
  }
]
Waiting for Task b6403848-e5f7-4ce4-a95c-87ef379d910d
{
  "rootId": "b6403848-e5f7-4ce4-a95c-87ef379d910d", 
  "serviceType": "Ztd Service", 
  "id": "b6403848-e5f7-4ce4-a95c-87ef379d910d", 
  "version": 1466501944693, 
  "startTime": 1466501944693, 
  "progress": "{\"message\":\"Success creating new site device(rule)\",\"ruleId\":\"20eabd09-2af7-40ac-9801-10b881b83f9a\"}", 
  "endTime": 1466501944730, 
  "isError": false
}

```
This is slightly more complex as I need to do a REST API call to map the project_name to a project_id and the file_name to file_id.
Again the call is async, so i need to poll the task.

You can look at the controller to see the project and the rules that have been created.
![uniq](pnp-screenshot.png?raw=true "uniq")
Similarly you can "list_project.py" to see the list of projects or "list_project.py Sydney-6130" to see the rules for a project.

## Clean up
Once you are done, you can run the "delete_file.py -a" and the "delete_project.py -a" to remove the files and the projects from the controller.
NOTE: you do not have to remove the rules as the arguments provided to the "delete_project" API call will remove all rules.

##Next Steps
This is an educational example where the steps have been broken out for clarity.  This does require some extra work in the code, as I have to lookup 
file and project names to resolve their UUID, where as an "all-in-one" version would keep the UUID of the resource that has been created.

 

