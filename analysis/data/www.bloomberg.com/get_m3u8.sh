#!/usr/bin/env bash

for file in *.out; do
    url=$( grep \.m3u8 $file | head -n 1)
    out=${file%%.*}
    wget -O ${out}.m3u8 $url
done
