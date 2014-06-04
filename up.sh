#!/bin/bash

# moves build files to a folder for background uploading. The out folder can be cleaned after
# as the build file is no longer residing there

if [[ -z $OUT_DIR_COMMON_BASE ]]; then
	out=$PWD"/out/target/product"
else
	out=$OUT_DIR_COMMON_BASE"/"${PWD##*/}"/target/product"
fi

device="$1"
up_dir="$2"
pacversion=$(grep 'ro.pacrom.version' $out/$device/system/build.prop | sed -e 's/ro.pacrom.version=//g')
rom="$pacversion".zip
md5="$rom".md5sum

mv /$out/$device/$md5 /home/langes/pac44/$up_dir/$md5
mv /$out/$device/$rom /home/langes/pac44/$up_dir/$rom

ncftpput -bb -f basket public_html/main/$device/nightly /home/langes/pac44/$up_dir/$md5
ncftpput -bb -f basket public_html/main/$device/nightly /home/langes/pac44/$up_dir/$rom
batchid=$(pgrep ncftpbatch)
if [[ -z $batchid ]]; then
    ncftpbatch -d
fi
