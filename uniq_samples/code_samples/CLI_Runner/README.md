This directory contains utilities for using the "CommandRunner"
API on APIC-EM.

It requires python3 for the uniq library.  It also requires version 1.4 of APIC-EM.
If you have downloaded an earlier version of uniq you will need to upgrade it.

I also recommend using virtualenv.  Use the following commands as examples

```buildoutcfg
virtualenv -p python3 env
source env/bin/activate
```

To install:

```buildoutcfg
pip install -r requirements.txt
```

You will need to edit the apic_config.py file to change your credentials.
NOTE:  You can also use environment variables for these parameters too.
   APIC, APIC_USER, APIC_PASSWORD will be looked at first.
   export APIC_PASSWORD="mysecrete" for example

To run:

There are some examples in the Examples file.
Note your IP address and tags will likely be different to those in the example.

```buildoutcfg
$ ./cmd_runner.py --ip 192.168.14.16 --command "show clock"
tag: None
['show clock']
[
  {
    "commandResponses": {
      "FAILURE": {},
      "BLACKLISTED": {},
      "SUCCESS": {
        "show clock": "20:44:40.509 UTC Sat Feb 25 2017"
      }
    },
    "deviceUuid": "5abffd04-f981-46be-8640-789af2e910d6"
  }
]

```

or for human friendly output (along with device selection using a tag)

```buildoutcfg

$ ./cmd_runner.py --tag iwan --command 'show ip nbar protocol-pack active |  inc Ver' --human
tag: iwan
['show ip nbar protocol-pack active |  inc Ver']
192.168.3.129: show ip nbar protocol-pack active |  inc Ver:
Version:                         28.0
NBAR Engine Version:             23
{}
192.168.13.1: show ip nbar protocol-pack active |  inc Ver:
Version:                         28.0
NBAR Engine Version:             23
{}
10.10.3.13: show ip nbar protocol-pack active |  inc Ver:
Version:                         28.0
NBAR Engine Version:             23
{}
10.10.2.13: show ip nbar protocol-pack active |  inc Ver:
Version:                         28.0
NBAR Engine Version:             23
{}


```