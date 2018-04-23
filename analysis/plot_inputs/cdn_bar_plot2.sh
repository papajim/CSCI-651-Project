#!/usr/bin/env bash

jpeg="cdn_bar_plot2.jpg"

gnuplot<<EOC
    reset
    set terminal jpeg size 1024,768
    set output "$jpeg"
    set style fill solid 0.5 border -1
    set boxwidth  0.5

    #set xtics rotate by 45 right
    #set xtics center offset 0,-2
    
    set title 'CDNs used by providers'
    set ylabel 'Providers (%)'
    set xlabel 'CDN' offset 0, -3

    set yrange [0:100]

    plot 'cdn_bar_plot2.in' using 1:3:xtic(2) notitle with boxes
EOC
