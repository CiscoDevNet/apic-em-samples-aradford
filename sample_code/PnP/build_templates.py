#!/usr/bin/env python
from __future__ import print_function
import jinja2
import csv
import sys
import os.path
from pnp_config import CONFIGS_DIR, TEMPLATE, DEVICES
from name_wrapper import name_wrap

def build_templates(template_file, devices):

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
            print("wrote file: %s" % config_filename)

    finally:
        f.close()
if __name__ == "__main__":
    build_templates(TEMPLATE, DEVICES)