# Introduction

This is a collection of sample scripts and tools for APIC-EM.

## Getting Started

Clone this repository:

``` bash
git clone https://github.com/CiscoDevNet/apic-em-samples-aradford.git
```

There are two different types of examples; tools and sample python code.

## tools/postman

[tools/postman](tools/postman/) contains a collection of [postman](https://www.getpostman.com/)
requests.  These use dynamic variables to link requests together.  This is particularly
useful for authentication and asychronous requests, where a `taskId` is returned.

## sample_code

[sample_code](sample_code/) contains some Python scripts to communicate with
Cisco's sandbox APIC-EM.  These scripts are written in Python 2 and use the third-party
[requests library](http://docs.python-requests.org/en/master/). They expose the
REST API structure and are a good tool for learning about the APIC-EM REST API.

There are examples for Plug-and-Play (PNP), inventory and EasyQoS (EQ).

## uniq_samples

[Uniq](https://github.com/CiscoDevNet/uniq) is a Python API client library for
APIC-EM, which abstracts the available REST API.  [uniq_samples](uniq_samples/)
contains some examples of using the library. You will need to install uniq to
use it, instructions for which are available in the uniq_samples directory README.

The Uniq library is written in Python 3.

*More to come...*
