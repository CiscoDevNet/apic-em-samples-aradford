from __future__ import print_function
import os.path
import random

fname="suffix.py"
if not os.path.isfile(fname):
    print('creating suffix')
    r = random.randint(1000,9999)
    with open(fname, 'a') as suffix_file:
        suffix_file.write('SUFFIX="%04d"\n' %r )
from suffix import SUFFIX

def name_wrap(name, fixed_len=False):
    
    #serial numbers are fixed length
    if fixed_len:
        return name[:-4] + SUFFIX
    else:
        return name + "-" + SUFFIX

