#!/bin/bash -e

# This file prepares a build environment and passes the devices to build for a build script
# that calls the build commands per device one-by-one

./sync
chmod a+x updates.sh
./updates.sh

device+=(anzu_a)
device+=(coconut_a)
device+=(haida_a)
device+=(hallon_a)
device+=(iyokan_a)
device+=(mango_a)
device+=(phoenix_a)
device+=(satsuma_a)
device+=(smultron_a)
device+=(urushi_a)
device+=(zeus_a)

./build.py -v ${device[@]}
