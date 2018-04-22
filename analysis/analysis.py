#!/usr/bin/env python

import os
import json
import glob


def create_bitrate_bar_plot(provider_info):
    return

def create_bitrate_box_plot(provider_info):
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
    with open(f, 'r') as g:
        provider_info[provider] = json.load(g)

print provider_info['www.bbc.com']
