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
    arguments are passed from a bash script
    (usually build-all.sh)
    cherry-picks are specified in another bash script file
    (usually cherries.sh) and this script calls repopick.py
    located in the /build/tools folder'''))
parser.add_argument('build', nargs='+', help='device to build with option switches')
parser.add_argument('-f', '--cherries', action='store_true', help='do a cherry-pick first')
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

# Get start time
ta = datetime.datetime.now().replace(microsecond=0)

# Create log file
lf = open('logs/build_log-%s.txt' % (ta), 'w')

# Fetch cherry-picks
if args.cherries:
    cmd = './cherries.sh'
    execute_cmd(cmd)

# Iterate through the requested devices
for argument in args.build:
    device, opt = argument.split('_', 1)

    # build device
    print('\nBuilding %s\n' % (device), file=lf)
    t1 = datetime.datetime.now().replace(microsecond=0)
    cmd = './build-pac.sh -%s %s' % (opt, device)
    execute_cmd(cmd)
    t2 = datetime.datetime.now().replace(microsecond=0)
    dt = (t2-t1)
    print('Build time for %s was: %s' % (device, dt), file=lf)

    # upload
    if not args.test:
        print('Uploading %s files' % (device), file=lf)
        cmd = ('./up.sh %s' % (device))
        subprocess.call(cmd, shell=True)
        t3 = datetime.datetime.now().replace(microsecond=0)
        dt = (t3-t2)
        print('Upload time for %s was: %s' % (device, dt), file=lf)

# Get duration
tz = datetime.datetime.now().replace(microsecond=0)
dt = (tz-ta)
print('\nBuild-bot time was: %s' % (dt), file=lf)
lf.close()
log = ('/home/langes/pac43/logs/build_log-%s.txt' % (ta))
fm = ('/var/www/users/langes/build_log-%s.txt' % (ta))
shutil.move(log, fm)
