#!/bin/bash

if [ -f ~/bin/paths-10.2.sh ]; then
    source ~/bin/paths-10.2.sh
fi

if [ "${android}" = "" ]; then
    android=~/pac43
fi
# camera: Fix preview on SEMC msm7x30 devices
cherries+=(48673_CM)

# libstagefright: extend support for disabling buffer metadata
cherries+=(56416_CM)

${android}/build/tools/repopick-new.py -b ${cherries[@]}
