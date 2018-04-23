#!/usr/bin/env bash

jpeg="protocol_bar_plot.jpg"

gnuplot<<EOC
    reset
    set terminal jpeg size 1024,768
    set output "$jpeg"
    set style fill solid 0.5 border -1
    set boxwidth  0.5
    set pointsize 0.5

    #set xtics rotate by 45 right
    #set xtics center offset 0,-2
    
    set title 'Number of providers using a protocol'
    set ylabel 'Number of providers'
    set xlabel 'Protocols'

    set yrange [0:12]

    plot 'protocol_bar_plot.in' using 1:3:xtic(2) notitle with boxes
EOC
