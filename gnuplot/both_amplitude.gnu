set terminal cairolatex standalone color colortext linewidth 2.5 size 4.5,2.4
set output "both_amplitude.tex"

set multiplot

set logscale

set tics front

xmin = 1.0e-22
xmax = 1.0e-13

f(m) = m*2.4e14 # frequency from mass
m(f) = f/2.4e14 # mass from frequency

#set xrange [f(xmin):f(xmax)]
set yrange [1e-20:3e-14]
set xrange [1e-5:1]

set ytics 10

set format x "${%T}$"
set format y "${%T}$"

# Ubuntu:
set margin 7,2,3,0.5
set ylabel '$\log_{10}|A|$'
set xlabel '$\log_{10}(f / \mathrm{Hz})$'  offset 0,+.4

# set key title "Cavities:\n"
set key at 4.0e-3, 1.0e-18
set key spacing 1.25

set style fill transparent solid 0.15 noborder

gps = "../gps_amplitudespectrum_data.txt"
file = "../cavity_amplitudespectrum_data.txt"

# set key font 6

set key title "Cavities\n"
set key at 4.0e-3, 1.0e-18
set key spacing 1.25

plot \
  file u 1:4 w l dt 1 lc "gray" t 'Detection threshold'\
  ,file u 1:3 w l dt 1 lc "coral" t '95\% confidence level'\
  ,file u 1:2 w l dt 1 lc "dark-red" t 'Amplitude'

# turn everything off for 2nd axis
unset xlabel     #label off
unset ylabel
set border 0      #border off
unset xtics       #tics off
unset ytics

set key title "GPS\n"
set key spacing 1.5
set key at 1.5e-0, 3.0e-15
set key Left
set key reverse

plot \
  gps u 1:3 w l dt 1 lc "#c73e04" t '95\% Confidence level'\
  ,gps u 1:2 w l dt 1 lc "#5C1C01" t 'Amplitude'
    
