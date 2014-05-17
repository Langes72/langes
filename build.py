#!/usr/bin/env python

from __future__ import print_function

import sys
import os
import subprocess
import re
import argparse
import textwrap
import datetime
import time
import os.path
import shutil

# Parse the command line
parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description=textwrap.dedent('''\
    a build-bot tool by Werner Gerber
    build arguments are passed from a bash script
    (usually build-all.sh)
    an upload script is called from here that moves
    successfull builds to a log folder so the out
    folder can safely be cleaned for the next build'''))
parser.add_argument('build', nargs='+', help='device to build with option switches')
parser.add_argument('-q', '--quiet', action='store_true', help='print as little as possible')
parser.add_argument('-t', '--test', action='store_true', help='test build, no uploads')
parser.add_argument('-v', '--verbose', action='store_true', help='print extra information to aid in debug')
args = parser.parse_args()
if args.quiet and args.verbose:
    parser.error('--quiet and --verbose cannot be specified together')

# Simple wrapper for os.system() that:
#   - exits on error
#   - prints out the command if --verbose
#   - suppresses all output if --quiet
def execute_cmd(cmd):
    if args.verbose:
        print('Executing: %s' % cmd, file=lf)
    if args.quiet:
        cmd = cmd.replace(' && ', ' &> /dev/null && ')
        cmd = cmd + " &> /dev/null"
    if os.system(cmd):
        if not args.verbose:
            print('\nCommand that failed:\n%s' % cmd, file=lf)
        sys.exit(1)

# Variables
out = 'out/target/product'
findn = 'ro.pacrom.version='

# Get start time
ta = datetime.datetime.now().replace(microsecond=0)
td = (time.strftime("%Y-%m-%d"))
up_dir = ('build_files_%s' % (td))
if not os.path.exists(up_dir):
    os.makedirs(up_dir)

# Create log file
lf = open('%s/build_log-%s.txt' % (up_dir, ta), 'w')
print('Building started at: %s' % (ta), file=lf)

# Iterate through the requested devices
for argument in args.build:
    # parse device and arguments
    device, opt = argument.split('_', 1)

    # build device
    print('\nBuilding %s\n' % (device))
    t1 = datetime.datetime.now().replace(microsecond=0)
    cmd = ('./build-pac.sh -%s %s' % (opt, device))
    with open('%s/%s-log' % (up_dir, device), 'w') as dlf:
        subprocess.call(cmd, stdout=dlf, stderr=subprocess.STDOUT, shell=True)
    t2 = datetime.datetime.now().replace(microsecond=0)
    dt = (t2-t1)

    # get build file names
    fname = '%s/%s/system/build.prop' % (out, device)
    if not os.path.isfile(fname):
        print('Building of %s failed' % (device), file=lf)
        continue;
    fl_prop = open(fname, "r")
    for line in fl_prop:
        if findn in line:
            PACVERSION = line.replace(findn, '').strip()
            rom = PACVERSION + '.zip'
            rompath = '%s/%s/%s' % (out, device, rom)
    if not os.path.isfile(rompath):
        print('Building of %s failed' % (device), file=lf)
        print('Build time for %s was: %s' % (device, dt), file=lf)
        continue;
    print('Build time for %s was: %s' % (device, dt), file=lf)

    # upload
    if not args.test:
        print('Uploading %s files' % (device), file=lf)
        cmd = ('./up.sh %s %s' % (device, up_dir))
        subprocess.call(cmd, shell=True)
        t3 = datetime.datetime.now().replace(microsecond=0)
        print('Upload added to spool at %s' % (t3), file=lf)

    # pause before starting next build
    time.sleep(5)

# Get duration
tz = datetime.datetime.now().replace(microsecond=0)
dt = (tz-ta)
print('\nBuild-bot time was: %s' % (dt), file=lf)
print('\nBuild-bot time was: %s' % (dt))
lf.close()
