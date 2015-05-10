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
rom="$3"
md5="$rom".md5sum

mv $out/$device/$md5 $up_dir/$md5
mv $out/$device/$rom $up_dir/$rom

ncftpput -bb -f basket $device/Unofficial $up_dir/$md5
ncftpput -bb -f basket $device/Unofficial $up_dir/$rom
batchid=$(pgrep ncftpspooler)
if [[ -z $batchid ]]; then
    ncftpbatch -d
fi
