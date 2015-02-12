#!/usr/bin/env python
# move subdirectories one level down

from __future__ import print_function

import sys
import os
import os.path
import subprocess
import shutil

# Where am I now
root = os.path.dirname(os.path.realpath(__file__))

# Where are we going
new_old_dir = 'KK'

# Lets do this
only_dirs = 1
device_dirs = os.walk(root).next()[only_dirs]
for device_dir in device_dirs:
    move_dirs = os.walk(device_dir).next()[only_dirs]
    for move_dir in move_dirs:
        source_dir = ('%s/%s/%s' % (root, device_dir, move_dir))
        dest_dir =  ('%s/%s/%s/%s' % (root, device_dir, new_old_dir, move_dir))
        print('Moving from %s to %s' % (source_dir, dest_dir))
        shutil.move(source_dir, dest_dir)

print('Done!')
