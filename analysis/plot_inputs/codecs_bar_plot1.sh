#!/usr/bin/env bash

jpeg="codecs_bar_plot1.jpg"

gnuplot<<EOC
    reset
    set terminal jpeg size 1024,768 font "Calibri,18"
    set output "$jpeg"
    set style data histogram
    set style histogram rowstacked
    set style fill solid 0.5 border -1
    set boxwidth  0.5

    set xtics rotate by 45 right
    set xtics center offset 0,-2
    
    set title 'Number of codecs used per provider'
    set ylabel 'Number of codecs'
    set xlabel 'Providers' offset 0, -3

    set yrange [0:10]

    plot 'codecs_bar_plot1.in' using 3:xtic(2) title "audio only", \
        '' using 4 title "video"
EOC
