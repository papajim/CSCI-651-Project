#!/usr/bin/env bash

jpeg="resolution_bar_plot3.jpg"

gnuplot<<EOC
    reset
    set terminal jpeg size 1024,768
    set output "$jpeg"
    set style fill solid 0.5 border -1
    set boxwidth  0.5

    set xtics rotate by 90 right
    set xtics center offset 0,-1.2
    set xtics font "Arial, 9"
    
    set title 'Number of providers offering a resolution'
    set ylabel 'Providers (%)'
    set xlabel 'Resolutions' offset 0, -2

    set yrange [0:100]

    plot 'resolution_bar_plot3.in' using 1:3:xtic(2) notitle with boxes
EOC
