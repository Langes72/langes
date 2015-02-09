#!/usr/bin/env python

# Made for PAC_ROM to trim the old nightlies from the file server (BasketBuild)
# checks the nightly folder of each device and deletes the oldest nightlies
# and their md5 files if there are more nightlies than specified

from __future__ import print_function

import sys
import os
import os.path
import argparse
import textwrap
import hashlib

# Parse the command line
parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description=textwrap.dedent('''\
A script that scans all subdirectories of its file location for the directory name specified in 'dir_del' \
and then scan those for the file types specified in 'extensions'
It will then count the files found in each directory and delete the oldest ones if/until there is 'max_zip' \
number of files left in that directory.
Can also be used to clean-up a specific directory where broken uploads are removed and missing md5 files are \
generated'''))
parser.add_argument('-m', '--max_zip', nargs=1, help='the number of files to keep')
parser.add_argument('-d', '--dir_del', nargs=1, help='the directory name to scan for')
parser.add_argument('-e', '--extensions', nargs=1, help='the file types to scan for')
parser.add_argument('-c', '--clean_up', nargs=1, help='removes broken uploads and creates missing md5 files')
args = parser.parse_args()
if not args.max_zip:
    args.max_zip = [10]
args.max_zip = int(args.max_zip[0])

if not args.dir_del:
    args.dir_del = ["nightly"]
args.dir_del = args.dir_del[0]

if not args.extensions:
    args.extensions = ['.zip', '.md5sum']

root = os.path.dirname(os.path.realpath(__file__))
to_small = 180000000

# Find all directories named nightly
def find_nightly_dirs():
    for path,dirs,files in os.walk(root):
        for d in dirs:
            if d == args.dir_del:
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
        if count > args.max_zip:
            zip_list.sort(key=lambda x: os.stat(x).st_mtime, reverse=True)
            print('Removing %s' % (zip_list[len(zip_list) - 1]))
            os.remove(zip_list.pop())
        else:
            to_many = False

# Iterate through the list of nightlies and call the count_zips function
# once for each file type specified in the extensions variable
def count_list(n_dirs):
    for d in n_dirs:
        for extension in args.extensions:
            count_zips(d, extension)

# Remove undersized zip files
def clean_broken(wdir):
    file_list = []
    file_list = os.listdir(wdir)
    for file in file_list:
        if file.endswith("zip"):
            if int(os.stat('%s/%s' % (wdir, file)).st_size) < to_small:
                print('Removing %s as it is undersized.' % (file))
                os.remove('%s/%s.md5sum' % (wdir, file))
                os.remove('%s/%s' % (wdir, file))

# Remove files with unmatching md5
def clean_malformed(wdir):
    file_list = []
    file_list = os.listdir(wdir)
    for file in file_list:
        if file.endswith('zip'):
            full_file = ('%s/%s' % (wdir, file))
            full_md5 = ('%s/%s.md5sum' % (wdir, file))
            if not os.path.isfile(full_md5):
                gen_md5file(full_file)
                print('Missing md5 file for %s created.' % (file))
            else:
                with open(full_md5, 'r') as md5_file:
                    file_md5 = md5_file.readline().split()
                if not file_md5[0] == read_md5sum(full_file):
                    os.remove(full_file)
                    os.remove(full_md5)
                    print('md5 of %s did not match and it was removed.' % (file))

# Read file md5sum
def read_md5sum(zip_file):
    with open(zip_file, 'rb') as check_md5:
        zip_data = check_md5.read()
        return hashlib.md5(zip_data).hexdigest()

# Create an md5 file
def gen_md5file(zip_file):
    md5_file = zip_file + '.md5sum'
    with open(md5_file, 'w') as new_file:
        new_file.write(read_md5sum(zip_file) + '  %s\n' % (os.path.basename(zip_file)))

if args.clean_up:
    ful_path = ('%s/%s' % (root, args.clean_up[0]))
    clean_broken(ful_path)
    clean_malformed(ful_path)
    sys.exit()

# Make a list of all the nightly directories
ndirs = list(find_nightly_dirs())

# Lets do this
count_list(ndirs)
