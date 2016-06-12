#Introduction

This is a collection of sample scripts and tools for APIC-EM.  

## Getting Started


### Download
Clone this repository:

``` bash
git clone https://github.com/CiscoDevNet/apic-em-samples-aradford.git
```

There are two different types of examples.  tools and sample python code

##tools/postman: 

[toosl/postman](tools/postman/) contains a collection of postman requests.  These use dynamic variables to link requests together.  This
is particularly useful for authentication and asychronous requests, where a taskId is returned.

##uniq_samples:
Uniq is a client library for APIC-EM.  [uniq_samples](uniq_samples/) contains some examples of using the library. This library
abstracts the REST API.  You will need to install uniq to use it.  Instructions for installation are also avaiable.

This library is written in python3

##sample_code:  

[sample_code](sample_code/)  contains some to talk to sandboxapic.  These scripts are written in python2 and use the requests
library.  They expose the REST API structure and are a good tool for learning about REST API.

There are examples for Plug-and-Play (PNP), inventory and EasyQoS (EQ).

More to come...
