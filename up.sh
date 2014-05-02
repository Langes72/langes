#!/bin/bash

device="$1"
up_dir="$2"
pacversion=$(grep 'ro.pacrom.version' /home/langes/pac44/out/target/product/$device/system/build.prop | sed -e 's/ro.pacrom.version=//g')
rom="$pacversion".zip
md5="$rom".md5sum

mv /home/langes/pac44/out/target/product/$device/$md5 /home/langes/pac44/$up_dir/$md5
mv /home/langes/pac44/out/target/product/$device/$rom /home/langes/pac44/$up_dir/$rom

ncftpput -bb -u pacman public_html/main/$device/nightly /home/langes/pac44/$up_dir/$md5
ncftpput -bb -u pacman public_html/main/$device/nightly /home/langes/pac44/$up_dir/$rom
batchid=$(pgrep ncftpbatch)
if [[ -z $batchid ]]; then
    ncftpbatch -d
fi
