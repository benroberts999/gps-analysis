set terminal cairolatex standalone color colortext linewidth 2.5 size 4.5,2.9
set output "dme.tex"

set logscale

set tics front

f(m) = m*2.4e14 # frequency from mass
m(f) = f/2.4e14 # mass from frequency

d_gps(A) = A*3.2e16 
d_cav(A) = A*3.6e21

xmin = 1.0e-20
xmax = 5.0e-14

# xmin = m(1.0e-6)
xmax = m(10)

set yrange [1e-4:1.0e7]
set xrange [xmin:xmax]

set xtics nomirror
set x2tics
set x2range [f(xmin):f(xmax)]

set ytics 10

set format x "${%T}$"
set format x2 "${%T}$"
set format y "${%T}$"

# Ubuntu:
set margin 7,2,3,3
set ylabel '$\log_{10}|d_{m_e}|$' offset -0.5
set xlabel '$\log_{10}(m_\phi / \mathrm{eV})$'  offset 0,+.2
set x2label '$\log_{10}(f / \mathrm{Hz})$' offset 0,-.2

# Mac:
# set margin 9,2,3.5,3.5
# set ylabel '$\log_{10}|d_{m_e}|$' offset -1.3
# set xlabel '$\log_{10}(m_\phi / \mathrm{eV})$'  offset 0,0
# set x2label '$\log_{10}(f / \mathrm{Hz})$' offset 0,-.1

set style fill transparent solid 0.15 noborder

# set label '\scriptsize{MICROSCOPE (EP)}' tc rgb 'gray50' at 1.2e-17,3e-3
# set label '\scriptsize{Yb/Cs}' tc rgb 'dark-blue' at 4e-20,2e-2
# set label '\scriptsize{H/Si}' tc rgb 'blue' at 1.4e-18,2e0
# set label '\scriptsize{H/Q/S}' tc rgb 'royalblue' at 3.3e-15,1.4e2
# set label '\scriptsize{Rb/Q}' tc rgb 'web-blue' at 8.0e-15,6e2

set label 'GPS (this work)' tc rgb 'white' at 3e-19,1e3 front
set label 'Cavities (this work)' tc rgb 'white' at 7e-18,1e6 front

set label '\small{Lab Clocks (projection)}' tc rgb 'dark-orange' at 1.2e-17,8e-1
set label '\small{Space Clocks (projection)}' tc rgb 'dark-green' at 1.2e-17,1.5e-3

tdt = 1

gps = "../gps_amplitudespectrum_data.txt"
file = "../cavity_amplitudespectrum_data.txt"

plot \
  file u (m($1)):(d_cav($3)) w l dt 1 lc "coral" lw 1.5 notitle\
  ,file u (m($1)):(d_cav($3)) w filledcurves x2 fillstyle transparent solid 0.7 lc "coral" notitle\
  ,gps u (m($1)):(d_gps($3)) w l dt 1 lc "#c73e04" lw 1.5 notitle\
  ,gps u (m($1)):(d_gps($3)) w filledcurves x2 fillstyle transparent solid 0.7 lc "#c73e04" notitle\
  ,"ProjectionLab.txt" w l dt 2 lc "dark-orange" lw 1.5 notitle\
  ,"ProjectionSpace.txt" w l dt 2 lc "dark-green" lw 1.5 notitle