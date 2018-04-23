#!/usr/bin/env python

import os
import json
import glob
import socket
import operator
from ipwhois import IPWhois

def create_bitrate_bar_plot(provider_info):
    with open('plot_inputs/bitrate_bar_plot.in', 'w+') as g:
        g.write("#seq provider avg_bitrate_num\n")
        counter = 1
        for provider in provider_info:
            avg_num_of_bitrates = 1.0*len(provider_info[provider]['bitrates_total'])/(1.0*len(provider_info[provider]['bitrates_list']))
            g.write("%d %s %0.2f\n" % (counter, provider, avg_num_of_bitrates))
            counter += 1
    return

def create_bitrate_box_plot(provider_info):
    header = "#"
    grid = []
    max_len = 0
    for provider in provider_info:
        header += provider + " "
        max_len = max(max_len, len(provider_info[provider]['bitrates_total']))
        
    for i in xrange(max_len):
        line = []
        for provider in provider_info:
            line.append('.')
        grid.append(line)

    j = 0
    for provider in provider_info:
        for i in xrange(len(provider_info[provider]['bitrates_total'])):
            grid[i][j] = str(provider_info[provider]['bitrates_total'][i])
        j += 1

    with open('plot_inputs/bitrate_box_plot.in', 'w+') as g:
        g.write(header+"\n")
        for i in xrange(max_len):
            g.write(" ".join(grid[i])+"\n")
    return

def create_codec_bar_plot(provider_info):
    codecs_usage = {}
    with open('plot_inputs/codecs_bar_plot1.in', 'w+') as g:
        g.write("#seq provider audio_codecs video_codecs\n")
        counter = 1
        for provider in provider_info:
            audio_counter = 0
            video_counter = 0
            codecs = provider_info[provider]['codec_list']
            for codec in codecs:
                if codec in codecs_usage:
                    codecs_usage[codec] += 1
                else:
                    codecs_usage[codec] = 1

                tmp = codec.split(',')
                if len(tmp) > 1 or "avc" in tmp[0]:
                    video_counter += 1
                elif "mp4a" in tmp[0]:
                    audio_counter += 1

            g.write("%d %s %d %d\n" % (counter, provider, audio_counter, video_counter))
            counter += 1

    with open('plot_inputs/codecs_bar_plot2.in', 'w+') as g:
        g.write("#seq codec num_of_providers\n")
        counter = 1
        for codec in sorted(codecs_usage.keys()):
            g.write("%d %s %d\n" % (counter, codec.replace(' ', ''), codecs_usage[codec]))
            counter += 1
        
    return

def create_cdn_bar_plot(provider_info):
    cdn_usage = {"Akamai": 0, "Fastly": 0, "Limelight": 0, "Brightcove": 0, "AmazonAWS": 0}
    total_providers = len(provider_info.keys())

    with open('plot_inputs/cdn_bar_plot1.in', 'w+') as g:
        g.write("#seq provider number_of_cdns\n")
        counter = 1
        for provider in provider_info:
            cdn_list = provider_info[provider]['cdn_list']
            g.write("%d %s %d\n" % (counter, provider, len(cdn_list)))
            #print "%s: %s" % (provider, " ".join(provider_info[provider]['cdn_list']))
            counter += 1
            
            distinct_cdns = set()
            for cdn in cdn_list:
                hostname = ""
                ip_addr = ""
                try:
                    #print cdn
                    ip_addr = socket.gethostbyname(cdn)
                    #print ip_addr
                    hostname = socket.gethostbyaddr(ip_addr)[0]
                except socket.herror:
                    print "SOCKET ERROR FOR %s, TRYING WHOIS" % cdn
                    obj = IPWhois(ip_addr)
                    result = obj.lookup_whois()
                    hostname = result['asn_description'].lower()

                if "akamai" in hostname:
                    distinct_cdns.add("Akamai")
                elif "fastly" in hostname:
                    distinct_cdns.add("Fastly")
                elif "llnw" in hostname:
                    distinct_cdns.add("Limelight")
                elif "brightcove" in hostname:
                    distinct_cdns.add("Brightcove")
                elif "amazonaws" in hostname:
                    distinct_cdns.add("AmazonAWS")
                else:
                    print "Unknown CDN"

            for cdn in distinct_cdns:
                cdn_usage[cdn] += 1
    
    with open('plot_inputs/cdn_bar_plot2.in', 'w+') as g:
        g.write("#seq cdn percentage_of_providers\n")
        counter = 1

        for cdn in sorted(cdn_usage.items(), key=operator.itemgetter(1)):
            g.write("%d %s %.2f\n" % (counter, cdn[0], (cdn[1]*1.0)/(total_providers*1.0)*100))
            counter += 1
    return

def create_chunk_targetduration_bar_plot(provider_info):
    target_durations = {}
    total_providers = len(provider_info.keys())
    
    with open('plot_inputs/chunk_targetduration_bar_plot1.in', 'w+') as g:
        g.write("#seq provider distinct_chunks\n")
        counter = 1
        for provider in provider_info:
            g.write("%d %s %d\n" % (counter, provider, len(provider_info[provider]['chunk_targetduration'])))
            for target in provider_info[provider]['chunk_targetduration']:
                if float(target) in target_durations:
                    target_durations[float(target)] += 1
                else:
                    target_durations[float(target)] = 1    
            counter += 1

    with open('plot_inputs/chunk_targetduration_bar_plot2.in', 'w+') as g:
        g.write("#seq chunk_duration percentage_of_providers\n")
        counter = 1

        for duration in sorted(target_durations.items(), key=operator.itemgetter(0)):
            g.write("%d %.2f %.2f\n" % (counter, duration[0], (duration[1]*1.0)/(total_providers*1.0)*100))
            counter += 1

    return

def create_resolution_bar_plot(provider_info):
    distinct_res_count = {}
    total_providers = len(provider_info.keys())
    with open('plot_inputs/resolution_bar_plot1.in', 'w+') as g:
        g.write("#seq provider avg_resolution_num\n")
        counter = 1
        for provider in provider_info:
            total_res = 0
            for resolutions in provider_info[provider]['resolutions_list']:
                total_res += len(resolutions)

            avg_num_of_resolutions = 1.0*total_res/(1.0*len(provider_info[provider]['resolutions_list']))

            g.write("%d %s %0.2f\n" % (counter, provider, avg_num_of_resolutions))
            counter += 1

    with open('plot_inputs/resolution_bar_plot2.in', 'w+') as g:
        g.write("#seq provider distinct_resolutions\n")
        counter = 1
        for provider in provider_info:
            g.write("%d %s %d\n" % (counter, provider, len(provider_info[provider]['resolutions_list_distinct'])))
            counter += 1
        
            for res in provider_info[provider]['resolutions_list_distinct']:
                if res in distinct_res_count:
                    distinct_res_count[res] += 1
                else:
                    distinct_res_count[res] = 1

    with open('plot_inputs/resolution_bar_plot3.in', 'w+') as g:
        g.write("#seq resolution percentage_of_providers\n")
        counter = 1

        for res in sorted(distinct_res_count.items(), key=operator.itemgetter(1)):
            g.write("%d %s %.2f\n" % (counter, res[0], (res[1]*1.0)/(total_providers*1.0)*100))
            counter += 1
    
    return

def create_protocol_bar_plot(provider_info):
    return


provider_info = {}
dirlist = glob.glob('*.json')
for f in dirlist:
    provider = f[:f.rfind('.')]
    provider = provider[provider.find('.')+1:provider.rfind('.')]
    with open(f, 'r') as g:
        provider_info[provider] = json.load(g)

create_bitrate_bar_plot(provider_info)
create_bitrate_box_plot(provider_info)
create_codec_bar_plot(provider_info)
create_cdn_bar_plot(provider_info)
create_chunk_targetduration_bar_plot(provider_info)
create_resolution_bar_plot(provider_info)
