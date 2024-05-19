#!/bin/bash
echo 'Filename: '$1;
gnuname=$1;
gnuplot $1;
imgfile=${gnuname/.gnu/};
imgfile=${1/.gnu/''}
convert -density 400 $imgfile-inc.pdf $imgfile-inc.png
convert -density 400 $imgfile-inc.png $imgfile-inc.pdf
texfile=${gnuname/gnu/tex};
texfile=${1/gnu/'tex'}
echo $texfile;
pdflatex $texfile;
pdflatex $texfile;
rm $texfile;
rm -f *-inc.eps *-inc.png *-inc-eps-* *-inc.pdf* *.aux *.log *.blg *.out *Notes.bib *.snm *.nav *.synctex.gz diagram.t1 *fdb_latexmk *.fls diagram.mp diagram.1 *.toc;
rm -f *.aux;
rm -f *.log;
rm -f *-inc.pdf;
rm -f *-inc.png;
