#!/usr/bin/env bash

jpeg="resolution_bar_plot1.jpg"

gnuplot<<EOC
    reset
    set terminal jpeg size 1024,768 font "Calibri,18"
    set output "$jpeg"
    set style fill solid 0.5 border -1
    set boxwidth  0.5
    set pointsize 0.5

    set xtics rotate by 45 right
    set xtics center offset 0,-2
    
    set title 'Average number of offered resolutions per video'
    set ylabel 'Average number of resolutions'
    set xlabel 'Providers' offset 0, -3

    set yrange [0:10]

    plot 'resolution_bar_plot1.in' using 1:3:xtic(2) notitle with boxes
EOC
