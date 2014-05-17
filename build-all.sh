#!/bin/bash -e

# This file passes the devices and the build arguments for a build script
# that calls the PAC-rom build script with the said arguments one-by-one

#devices to build
device+=(anzu_c1)
device+=(coconut_c1)
device+=(haida_c1)
device+=(hallon_c1)
device+=(iyokan_c1)
device+=(mango_c1)
device+=(satsuma_c1)
device+=(smultron_c1)
device+=(urushi_c1)

./langes/build.py -v ${device[@]}
