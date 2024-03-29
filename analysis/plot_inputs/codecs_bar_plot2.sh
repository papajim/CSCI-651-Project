#!/usr/bin/env bash

jpeg="codecs_bar_plot2.jpg"

gnuplot<<EOC
    reset
    set terminal jpeg size 1024,768 font "Calibri,18"
    set output "$jpeg"
    set style fill solid 0.5 border -1
    set boxwidth  0.5

    set xtics rotate by 45 right
    set xtics center offset 0,-4
    set xtics font "Calibri, 10"
    
    set title 'Number of providers offering a codec'
    set ylabel 'Providers'
    set xlabel 'Codecs' offset 0, -6.5

    set yrange [0:8]

    plot 'codecs_bar_plot2.in' using 1:3:xtic(2) notitle with boxes
EOC
