#!/bin/bash -e

# This file passes the devices and the build arguments for a build script
# that calls the PAC-rom build script with the said arguments one-by-one

#devices to build
device+=(anzu_co3)
device+=(coconut_co3)
device+=(haida_co3)
device+=(hallon_co3)
device+=(iyokan_co3)
device+=(mango_co3)
device+=(satsuma_co3)
device+=(smultron_co3)
device+=(urushi_co3)

./build.py -v ${device[@]}
