#!/usr/bin/env bash

jpeg="chunk_targetduration_bar_plot1.jpg"

gnuplot<<EOC
    reset
    set terminal jpeg size 1024,768
    set output "$jpeg"
    set style fill solid 0.5 border -1
    set boxwidth  0.5
    set pointsize 0.5

    set xtics rotate by 45 right
    set xtics center offset 0,-2
    
    set title 'Distinct chunk duration discovered per provider'
    set ylabel 'Number of chunk durations'
    set xlabel 'Providers' offset 0, -3
    set yrange [0:4]

    plot 'chunk_targetduration_bar_plot1.in' using 1:3:xtic(2) notitle with boxes
EOC
