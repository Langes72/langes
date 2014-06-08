#!/bin/bash -e

# This file passes the devices and the build arguments for a build script
# that calls the PAC-rom build script with the said arguments one-by-one

#devices to build
device+=(anzu_fc3)
device+=(coconut_c3)
device+=(haida_c3)
device+=(hallon_c3)
device+=(iyokan_c3)
device+=(mango_c3)
device+=(satsuma_c3)
device+=(smultron_c3)
device+=(urushi_c3)

./langes/build.py -v ${device[@]}
