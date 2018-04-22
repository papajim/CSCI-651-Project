#!/usr/bin/env bash

jpeg="bitrate_bar_plot.jpg"

gnuplot<<EOC
    reset
    set terminal jpeg size 1024,768
    set output "$jpeg"
    set style fill solid 0.5 border -1
    set boxwidth  0.5
    set pointsize 0.5

    set xtics rotate by 45 right
    set xtics center offset 0,-2
    
    set title 'Total number of offered bitrates by content provider'
    set ylabel 'Number of Bitrates'
    set xlabel 'Providers' offset 0, -3

    plot 'bitrate_bar_plot.in' using 1:3:xtic(2) notitle with boxes
EOC
