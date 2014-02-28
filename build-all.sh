#!/bin/bash -e

# This file passes the devices and the build arguments for a build script
# that calls the PAC-rom build script with the said arguments one-by-one

#devices to build
device+=(anzu_fcio3)
device+=(coconut_io3)
device+=(haida_io3)
device+=(hallon_io3)
device+=(iyokan_io3)
device+=(satsuma_io3)
device+=(smultron_io3)
device+=(urushi_io3)

#Setup log file and log terminal output
t1=$(date +%d-%m-%y_%R)
exec >> "logs/${t1}.log" #2>&1

./build.py -v ${device[@]}
