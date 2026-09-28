# Use latexmk for robust compilation
LATEXMK = latexmk
FLAGS = -pdf -pvc- -file-line-error

# Main source file
# Remplacez ficheMatiere.tex par la fiche à compiler
SRC = ./formation_git.tex

# PDF output file
PDF = $(SRC:.tex=.pdf)

# Default target: compile the PDF
all: $(PDF)

# Rule to build the PDF
$(PDF): $(SRC)
	$(LATEXMK) $(FLAGS) $(SRC)

# Target to open the generated PDF
view: all
	xdg-open $(PDF) &

# Target to clean up auxiliary files
clean:
	$(LATEXMK) -C
	rm -f *.nav  *.snm *.vrb

.PHONY: all view clean
