#!/bin/bash -e

# This file passes the devices and the build arguments for a build script
# that calls the PAC-rom build script with the said arguments one-by-one

#devices to build
device+=(anzu_ci)
device+=(coconut_i)
device+=(haida_i)
device+=(hallon_i)
device+=(iyokan_ci)
device+=(satsuma_i)
device+=(smultron_i)
device+=(urushi_i)

#Setup log file and log terminal output
t1=$(date +%d-%m-%y_%R)
exec >> "logs/${t1}.log" #2>&1

./build.py -fv ${device[@]}
