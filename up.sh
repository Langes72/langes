#!/bin/bash

# moves build files to a folder for background uploading. The out folder can be cleaned after
# as the build file is no longer residing there

device="$1"
up_dir="$2"
lxversion=$(grep 'ro.cm.version' /mnt/out/langes/lx/target/product/$device/system/build.prop | sed -e 's/ro.cm.version=//g')
rom=cm-"$lxversion".zip
md5="$rom".md5sum

mv /mnt/out/langes/lx/target/product/$device/$md5 /home/langes/lp/lx/$up_dir/$md5
mv /mnt/out/langes/lx/target/product/$device/$rom /home/langes/lp/lx/$up_dir/$rom

ncftpput -bb -f basket $device/cm-12.1 /home/langes/lp/lx/$up_dir/$md5
ncftpput -bb -f basket $device/cm-12.1 /home/langes/lp/lx/$up_dir/$rom
batchid=$(pgrep ncftpbatch)
if [[ -z $batchid ]]; then
    ncftpbatch -d
fi

rm -rf /mnt/out/langes/lx/target/product/$device
