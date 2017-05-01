

ping $1 | grep --color=auto -Po "time=\d+" --line-buffered | grep --color=auto -Po '\d+' --line-buffered > ping.dat &

redraw() {
    count=$(wc -l ping.dat | cut -d' ' -f1)

    xmin=$(( count<20?0:count-20 ))
    xmax=$(( count<20?20:count ))

    gnuplot <<CMDS
    reset
    set xrange [${xmin}:${xmax}]
    set yrange [0:*]

    set border lw 2 lc rgb "grey"

    set xtics textcolor rgb "white"
    set ytics textcolor rgb "white"

    set xlabel "Pings" textcolor rgb "white" font "Arial,10"
    set ylabel "Latency" textcolor rgb "white" font "Arial,10"

    set grid

    set grid xtics lc rgb "#dbdbdb" lw 1 lt 0
    set grid ytics lc rgb "#dbdbdb" lw 1 lt 0

    set key textcolor rgb "white" font "Arial,10"

    # set samples 200

    # stats "ping.dat"

    # set terminal unknown
    set term sixel small color size 600,300
    plot "ping.dat" smooth unique with lines

    set yrange [0:GPVAL_Y_MAX*1.50]

    set label 1 tc rgb "white"
    set label 1 gprintf("Maximum: %g", GPVAL_Y_MAX) center at first GPVAL_Y_MAX, GPVAL_Y_MAX point

    replot
CMDS
}

while true; do
    redraw
    sleep 1
done
