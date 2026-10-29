# LaTeX Makefile for npj Microgravity manuscript

TARGET = main

all: pdf

pdf:
	pdflatex -interaction=nonstopmode $(TARGET).tex
	bibtex $(TARGET)
	pdflatex -interaction=nonstopmode $(TARGET).tex
	pdflatex -interaction=nonstopmode $(TARGET).tex

clean:
	rm -f *.aux *.bbl *.blg *.log *.out *.toc *.synctex.gz *.fls *.fdb_latexmk

distclean: clean
	rm -f $(TARGET).pdf

.PHONY: all pdf clean distclean
