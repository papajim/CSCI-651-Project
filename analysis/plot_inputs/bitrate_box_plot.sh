#!/usr/bin/env bash

jpeg="bitrate_box_plot.jpg"

gnuplot<<EOC
    reset
    set terminal jpeg size 1024,768 font "Calibri,18"
    set output "$jpeg"
    set style fill solid 0.5 border -1
    set style boxplot outliers pointtype 7
    set style data boxplot
    set boxwidth  0.5
    set pointsize 0.5

    HEADER="`head -1 bitrate_box_plot.in | cut -b 2-`"
    set for [i=1:words(HEADER)] xtics ( word(HEADER,i) i ) rotate by 45 right
    set xtics center offset 0,-2
    
    set title 'Distribution of bitrates used by content provider'
    set ylabel 'Bitrate (bits/sec)'
    set xlabel 'Providers' offset 0, -3

    plot for [i=1:15] 'bitrate_box_plot.in' using (i):i notitle
EOC
