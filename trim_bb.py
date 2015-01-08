#!/usr/bin/env python

# Made for PAC_ROM to trim the old nightlies from the file server (BasketBuild)
# checks the nightly folder of each device and deletes the oldest nightlies
# and their md5 files if there are more nightlies than specified

from __future__ import print_function

import sys
import os
import os.path

max_zip = 10
extensions = ['.zip', '.md5sum']
root = os.path.dirname(os.path.realpath(__file__))

# Find all directories named nightly
def find_nightly_dirs():
    for path,dirs,files in os.walk(root):
        for d in dirs:
            if d == "nightly":
                yield os.path.join(path, d)

# Count the number of files of a type and recursively remove the oldest one
# until the count equals the max_zip variable
def count_zips(n_dir, extension):
    to_many = True
    while to_many == True:
        file_list = []
        zip_list = []
        file_list = os.listdir(n_dir)
        count = 0
        for file in file_list:
            if file.endswith(extension):
                count += 1
                zip_list.append(n_dir + "/" + file)
        if count > max_zip:
            zip_list.sort(key=lambda x: os.stat(x).st_mtime, reverse=True)
            print('Removing %s' % (zip_list[len(zip_list) - 1]))
            os.remove(zip_list.pop())
        else:
            to_many = False

# Iterate through the list of nightlies and call the count_zips function
# once for each file type specified in the extensions variable
def count_list(n_dirs):
    for d in n_dirs:
        for extension in extensions:
            count_zips(d, extension)

# Make a list of all the nightly directories
ndirs = list(find_nightly_dirs())

# Lets do this
count_list(ndirs)
