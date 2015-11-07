#!/bin/bash

usage()
{
    echo -e ""
    echo -e "Usage:"
    echo -e "  build-lx.sh [options] device"
    echo -e ""
    echo -e "  Options:"
    echo -e "    -c  Clean before build"
    echo -e "    -f  Fetch cherries"
    echo -e "    -m  Refresh manifests"
    echo -e "    -s  Sync before build"
    echo -e ""
    echo -e "  Example:"
    echo -e "    ./build-lx.sh -c urushi"
    echo -e ""
    exit 1
}


OUT_DIR=/mnt/out/langes/lx

if [ ! -d ".repo" ]; then
    echo -e "No .repo directory found.  Is this an Android build tree?"
    exit 1
fi

if [ "${android}" = "" ]; then
    android="${PWD}"
fi


# get time of startup
DATE=date
t1=$($DATE '+%s')

opt_a=0
opt_clean=0
opt_fetch=0
opt_man=0
opt_sync=0

while getopts "acfms" opt; do
    case "$opt" in
    a) opt_a=1 ;;
    c) opt_clean=1 ;;
    f) opt_fetch=1 ;;
    m) opt_man=1 ;;
    s) opt_sync=1 ;;
    *) usage
    esac
done
shift $((OPTIND-1))
if [ "$#" -ne 1 ]; then
    usage
fi
device="$1"

if [ "$opt_clean" -ne 0 ]; then
    make clean >/dev/null
    echo -e ""
    echo -e "Out is clean"
    echo -e ""
fi

if [ "$opt_man" -ne 0 ]; then
    repo sync vendor/extra
    opt_sync=1
    cp -f $android/vendor/extra/semc.xml $android/.repo/local_manifests/semc.xml
    cp -f $android/vendor/extra/extra.xml $android/.repo/local_manifests/extra.xml
    cp -f $android/vendor/extra/updates.sh $android/updates.sh
    echo -e ""
    echo -e "Manifests etc. updated"
    echo -e ""
fi

if [ "$opt_fetch" -ne 0 ]; then
    repo abandon auto
fi

if [ "$opt_sync" -ne 0 ]; then
    repo sync -j16
    echo -e ""
    echo -e "Source is fresh"
    echo -e ""
fi

if [ "$opt_fetch" -ne 0 ]; then
    chmod a+x updates.sh
    ./updates.sh
    echo -e "Standard cherries picked"
    echo -e ""
fi

if [ -z "${USE_PREBUILT_CHROMIUM}" ]; then
    export USE_PREBUILT_CHROMIUM=1
fi

rm -f $OUT_DIR/target/product/$device/system/build.prop

# get time of prep
t2=$($DATE +%s)

export USE_CCACHE=1
export CCACHE_DIR=/home/langes/.ccache/cm12
ccache -M 50G

. build/envsetup.sh
lunch cm_$device-userdebug
make -j8 bacon

# get time of end
t3=$($DATE +%s)
tpmin=$(( (t2-t1)/60 ))
tpsec=$(( (t2-t1)%60 ))
tbmin=$(( (t3-t2)/60 ))
tbsec=$(( (t3-t2)%60 ))
ttmin=$(( (t3-t1)/60 ))
ttsec=$(( (t3-t1)%60 ))

echo -e ""
echo -e "Prep time:${txtrst} ${grn}$tpmin minutes $tpsec seconds"
echo -e "Build time:${txtrst} ${grn}$tbmin minutes $tbsec seconds"
echo -e "Total time${txtrst} ${grn}$ttmin minutes $ttsec seconds"
