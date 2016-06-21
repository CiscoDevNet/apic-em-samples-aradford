# Uniq Sample code
Uniq is a python3 client library for APIC-EM.  This directory contains some sample scripts in 
[code_samples](code_samples/).  To use these samples, you first need to install uniq.  It is recommended that you use
a virtualenv to do this.  This is only a recommendation, not a requirement.

### Download
Clone the uniq repository:

``` bash
git clone https://github.com/CiscoDevNet/uniq.git
```

### Install a virtualenv
This optional step will create a virtual environment for uniq

``` bash
virtualenv -p python3 env
source env/bin/activate
```

### Install
Then install the package locally.

``` bash
cd uniq
python3 setup.py install
```
Note: if you see an error message 
``` bash
copying apis/nb/clients/topology_client/vrf.json -> build/lib/uniq/apis/nb/clients/topology_client
error: can't copy 'opyright': doesn't exist or not a regular file

```
You need to update your installtools

``` bash
$ pip3 install -U setuptools
```

### Use
Just need to change into the appropriate directory and run the scripts

``` bash

# if you were in the uniq installation directory
$ cd .. 

$ ls
README.md	__init__.py	code_samples uniq env

$ cd code_samples

# now you can run the first example
$ python3 00_get_network_device.py 
IP Address       Device Name     
55.1.1.3         AP7081.059f.19ca
212.1.10.1       CAMPUS-Access1  
10.204.61.2      CAMPUS-Core1    
211.2.1.1        CAMPUS-Core2    
212.1.10.100     CAMPUS-Dist1    
212.1.20.2       CAMPUS-Dist2    
210.1.1.1        CAMPUS-Router1  
210.2.1.1        CAMPUS-Router2  
55.1.1.2         Campus-WLC-5508 

```

