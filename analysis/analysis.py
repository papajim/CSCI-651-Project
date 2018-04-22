#!/usr/bin/env python

import os
import json
import glob


def create_bitrate_bar_plot(provider_info):
    with open('plot_inputs/bitrate_bar_plot.in', 'w+') as g:
        g.write("#seq provider bitrate_num\n")
        counter = 1
        for provider in provider_info:
            g.write("%d %s %d\n" % (counter, provider, len(provider_info[provider]['bitrates_total'])))
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

def create_cdn_pie_chart(provider_info):
    return

def create_chunk_targetduration_bar_plot(provider_info):
    return

def create_resolution_bar_plot(provider_info):
    return

def create_protocol_pie_chart1(provider_info):
    return

def create_protocol_pie_chart2(provider_info):
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
