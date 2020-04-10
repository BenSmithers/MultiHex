#!/usr/bin/python3

import MultiHex
import os
from glob import glob

"""
This writes a bash script to call pydoc enough times to build html documentation of MultiHex! 
"""

def get_cont(where):
    """
    Gets the name of the python files inside a directory. 

    Removes the ".py" part
    """
    files = glob(where + "*.py")
    for i in range(len(files)):
        files[i] = files[i].split("/")[-1]
        files[i] = files[i].split(".")[0]
    return(files)

print("Generating bash script to make the docs")

fl_name = "gen_docs.sh"

if os.path.isfile("./"+fl_name):
    os.remove("./"+fl_name)
obj = open(fl_name,'w')

loc = MultiHex.__file__
loc = "/".join(loc.split("/")[:-1]) + "/"

obj.write("#!/bin/bash\n")
obj.write("pydoc3 -w MultiHex\n")
for entry in get_cont(loc):
    if entry=="__init__":
        continue
    obj.write("pydoc3 -w MultiHex."+entry+"\n")

def write_sub(this):
    """
    Add lines to document the sub-directories
    """
    obj.write("pydoc3 -w MultiHex.{}\n".format(this))
    for entry in get_cont(loc+"/"+this+"/"):
        if entry=="__init__":
            continue
        obj.write("pydoc3 -w MultiHex.{}.{}\n".format(this, entry))

write_sub("generator")
write_sub("guis")
write_sub("map_types")
write_sub("tests")

obj.close()

os.chmod( fl_name, 0o777)
print("Now call `./gen_docs.sh`")
