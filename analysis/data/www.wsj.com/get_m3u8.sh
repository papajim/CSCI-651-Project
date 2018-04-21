#!/usr/bin/env bash

for file in *.m3u8; do
    file=${file%.*}.out
    url=$( grep "\.m3u8$" $file | head -n 1)
    #url=${url##*?u=}
    out=${file%.*}
    wget -O ${out}.m3u8 "$url"
done
