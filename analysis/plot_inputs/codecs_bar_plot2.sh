#!/usr/bin/env bash

jpeg="codecs_bar_plot2.jpg"

gnuplot<<EOC
    reset
    set terminal jpeg size 1024,768
    set output "$jpeg"
    set style fill solid 0.5 border -1
    set boxwidth  0.5

    set xtics rotate by 90 right
    set xtics center offset 0,-4
    set xtics font "Arial, 9"
    
    set title 'Number of providers offering a codec'
    set ylabel 'Providers'
    set xlabel 'Codecs' offset 0, -6.5

    set yrange [0:7]

    plot 'codecs_bar_plot2.in' using 1:3:xtic(2) notitle with boxes
EOC
