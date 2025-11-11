# Makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = .
BUILDDIR      = _build

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

# Build HTML documentation
html:
	@echo "Building HTML documentation..."
	@$(SPHINXBUILD) -b html "$(SOURCEDIR)" "$(BUILDDIR)/html" $(SPHINXOPTS)
	@echo "Build finished. The HTML pages are in $(BUILDDIR)/html."

# Build HTML with warnings as errors (strict mode)
html-strict:
	@echo "Building HTML documentation (strict mode)..."
	@$(SPHINXBUILD) -W -b html "$(SOURCEDIR)" "$(BUILDDIR)/html" $(SPHINXOPTS)
	@echo "Build finished. The HTML pages are in $(BUILDDIR)/html."

# Clean build directory
clean:
	@echo "Cleaning build directory..."
	@rm -rf "$(BUILDDIR)"
	@echo "Clean finished."

# Clean and rebuild
rebuild: clean html

# Show all warnings
warnings:
	@echo "Building with verbose warnings..."
	@$(SPHINXBUILD) -v -b html "$(SOURCEDIR)" "$(BUILDDIR)/html" $(SPHINXOPTS)

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
