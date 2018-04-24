#!/usr/bin/env bash

jpeg="chunk_targetduration_bar_plot2.jpg"

gnuplot<<EOC
    reset
    set terminal jpeg size 1024,768 font "Calibri,18"
    set output "$jpeg"
    set style fill solid 0.5 border -1
    set boxwidth  0.5

    #set xtics rotate by 45 right
    #set xtics center offset 0, 0
    
    set title 'Chunk durations used by providers'
    set ylabel 'Providers (%)'
    set xlabel 'Chunk duration (seconds)' offset 0, 0

    set yrange [0:100]

    plot 'chunk_targetduration_bar_plot2.in' using 1:3:xtic(2) notitle with boxes
EOC
