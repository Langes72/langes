#!/bin/bash

# moves build files to a folder for background uploading. The out folder can be cleaned after
# as the build file is no longer residing there

device="$1"
up_dir="$2"
lxversion=$(grep 'ro.cm.version' /mnt/out/langes/system/target/product/$device/system/build.prop | sed -e 's/ro.cm.version=//g')
rom=cm-"$lxversion".zip
md5="$rom".md5sum

mv /mnt/out/langes/system/target/product/$device/$md5 /home/langes/android/system/$up_dir/$md5
mv /mnt/out/langes/system/target/product/$device/$rom /home/langes/android/system/$up_dir/$rom

if $DO_UP; then
    ncftpput -bb -f basket $device/cm-11.0/nightlies /home/langes/android/system/$up_dir/$md5
    ncftpput -bb -f basket $device/cm-11.0/nightlies /home/langes/android/system/$up_dir/$rom
    batchid=$(pgrep ncftpbatch)
    if [[ -z $batchid ]]; then
        ncftpbatch -d
    fi
fi

rm -rf /mnt/out/langes/system/target/product/$device
