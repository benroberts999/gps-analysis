set terminal cairolatex standalone color colortext linewidth 2.5 size 4.5,3.25
set output "gps_amplitude.tex"

set logscale

set tics front

xmin = 1.0e-22
xmax = 1.0e-13

f(m) = m*2.4e14 # frequency from mass
m(f) = f/2.4e14 # mass from frequency
d(A) = A*8.25e16 # coupling from Amplitude (not stochastic)

#set xrange [f(xmin):f(xmax)]
# set yrange [:2e-15]
# set yrange [:1e-13]
set xrange [1e-5:1e-1]

set ytics 10

set format x "${%T}$"
set format y "${%T}$"

# Ubuntu:
set margin 7,2,3,3
set ylabel '$\log_{10}|A|$'
set xlabel '$\log_{10}(f / \mathrm{Hz})$'  offset 0,+.4
# set key at 4.0e-3, 1.8e-18
set key spacing 1.25

# Mac:
# set margin 9,2,3.5,3.5
# set ylabel '$\log_{10}|A|$' offset -1.3,0
# set xlabel '$\log_{10}(f / \mathrm{Hz})$' offset 0,0
# set key bottom left
# set key spacing 1.5

set style fill transparent solid 0.15 noborder



gps = "../gps_amplitudespectrum_data.txt"
file = "../cavity_amplitudespectrum_data.txt"

plot \
  gps u 1:3 w l dt 1 lc "#c73e04" t 'GPS 95\% confidence level'\
  ,gps u 1:2 w l dt 1 lc "#5C1C01" t 'GPS Amplitude'
