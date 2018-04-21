#!/usr/bin/env python

import os
import glob
import json
import requests

providers = ['video.foxnews.com']
#             'www.bloomberg.com',
#             'www.cnbc.com',
#             'www.huffingtonpost.com',
#             'www.nbcolympics.com',
#             'www.nytimes.com',
#             'www.usatoday.com',
#             'www.wsj.com',
#             'www.cbssports.com',
#             'www.cnn.com',
#             'www.espn.com',
#             'www.nba.com',
#             'www.premierleague.com',
#             'www.weather.com',
#             'www.wwe.com']
#             'www.cricbuzz.com',
#             'www.bbc.com',
#             'www.nhl.com',

for provider in providers:
    provider_info = {}
    protocols = set()
    bitrates_list = []
    bitrates_total = []
    bitrates_avg_list = []
    bitrates_avg_total = []
    resolutions_list = []
    resolutions_list_distinct = []
    codec_list = set()
    audio_only_streams = 0
    cdn_list = set()
    chunksize_list = []
    chunksize_list_distinct = []
    hls_version_list = set()

    input_folder = 'data/' + provider
    dirlist = glob.glob(input_folder+'/*')
    
    for f in dirlist:
        bitrates = []
        bitrates_avg = []
        resolutions = set()
        chunksize = set()

        if os.stat(f).st_size == 0 or f.endswith('.out'):
            continue

        if f.endswith('.m3u8'):
            protocols.add('HLS')
        elif f.endswith('.mpd'):
            protocols.add('MPEG-DASH')

        #NO MPD PARSE FOR NOW
        lines = []
        with open(f, "r") as g:
            lines = g.readlines()

        for line in lines:
            if line.startswith('#EXT-X-STREAM-INF'):
                stats = line[line.find(':')+1:].split(',')

                for k in xrange(len(stats)):
                    if stats[k].startswith('BANDWIDTH'):
                        value = stats[k].split('=')[1]
                        bitrates.append(int(value))
                    elif stats[k].startswith('AVERAGE-BANDWIDTH'):
                        value = stats[k].split('=')[1]
                        bitrates_avg.append(int(value))
                    elif stats[k].startswith('RESOLUTION'):
                        value = stats[k].split('=')[1].replace('\n', '')
                        resolutions.add(value)
                    elif stats[k].startswith('CODECS'):
                        if k < len(stats) - 1:
                            stats[k] += "," + stats[len(stats)-1]
                        value = stats[k].split('=')[1]
                        value = value.replace('\n', '')
                        value = value.replace('"', '')
                        codec_list.add(value)
                        #if not ',' in value:
                        #    audio_only_streams += 1
            elif not line.startswith('#') and not line == "":
                sub_manifest = None
                if line.startswith('http'):
                    cdn_start = line.find('//')
                    cdn_stop = line.find('/', cdn_start+2)
                    cdn = line[cdn_start+2:cdn_stop]
                    cdn_list.add(cdn)
                    sub_manifest = requests.get(line).text
                    #print sub_manifest
                #else:
                    #not yet implented

                if sub_manifest is None:
                    #print f
                    print "Sub Manifest file is not defined"
                    exit()

                sub_manifest = sub_manifest.split("\n")
                for record in sub_manifest:
                    if record.startswith('#EXT-X-VERSION'):
                        hls_version_list.add(int(record.split(':')[1]))
                    elif record.startswith('#EXTINF'):
                        chunksize.add(float(record.split(':')[1][:-1]))

        bitrates_list.append(bitrates)
        bitrates_avg_list.append(bitrates_avg)
        resolutions_list.append(list(resolutions))
        chunksize_list.append(list(chunksize))

    for l in bitrates_list:
        bitrates_total += l
    bitrates_total.sort()

    for l in bitrates_avg_list:
        bitrates_avg_total += l
    bitrates_avg_total.sort()

    for l in resolutions_list:
        resolutions_list_distinct += list(l)
    resolutions_list_distinct = set(resolutions_list_distinct)
    resolutions_list_distinct = sorted(resolutions_list_distinct)

    for l in chunksize_list:
        chunksize_list_distinct += list(l)
    chunksize_list_distinct = set(chunksize_list_distinct)
    chunksize_list_distinct = sorted(chunksize_list_distinct)

    provider_info['protocols'] = list(protocols)
    provider_info['bitrates_list'] = bitrates_list
    provider_info['bitrates_total'] = bitrates_total
    provider_info['bitrates_avg_list'] = bitrates_avg_list
    provider_info['bitrates_avg_total'] = bitrates_avg_total
    provider_info['resolutions_list'] = resolutions_list
    provider_info['resolutions_list_distinct'] = resolutions_list_distinct
    provider_info['codec_list'] = list(codec_list)
    provider_info['cdn_list'] = list(cdn_list)
    provider_info['chunksize_list'] = chunksize_list
    provider_info['chunksize_list_distinct'] = chunksize_list_distinct
    provider_info['hls_version_list'] = list(hls_version_list)

    with open(provider+'.json', 'w+') as g:
        json.dump(provider_info, g, sort_keys=True, indent=2)
