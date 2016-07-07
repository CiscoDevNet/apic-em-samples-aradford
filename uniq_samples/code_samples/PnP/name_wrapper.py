from __future__ import print_function
import os.path
import random
from pnp_config import USE_NAME_WRAP

fname="suffix.py"
if not os.path.isfile(fname):
    print('creating suffix')
    r = random.randint(1000,9999)
    with open(fname, 'a') as suffix_file:
        suffix_file.write('SUFFIX="%04d"\n' %r )
from suffix import SUFFIX

# this is a wrapper function to create unique names for projects and files
# it is required if doing shared labs on a controller.
# it can be turned off by modifying the USE_NAME_WRAP variable in the pnp_config file
def name_wrap(name, fixed_len=False):
    if not USE_NAME_WRAP:
        return name
    #serial numbers are fixed length
    if fixed_len:
        return name[:-4] + SUFFIX
    else:
        return name + "-" + SUFFIX

