#!/usr/bin/env bash

jpeg="resolution_bar_plot2.jpg"

gnuplot<<EOC
    reset
    set terminal jpeg size 1024,768
    set output "$jpeg"
    set style fill solid 0.5 border -1
    set boxwidth  0.5
    set pointsize 0.5

    set xtics rotate by 45 right
    set xtics center offset 0,-2
    
    set title 'Distinct number of offered resolutions per provider'
    set ylabel 'Number of resolutions'
    set xlabel 'Providers' offset 0, -3

    set yrange [0:13]

    plot 'resolution_bar_plot2.in' using 1:3:xtic(2) notitle with boxes
EOC
