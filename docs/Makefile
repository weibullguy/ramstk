# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
SOURCEDIR     = .
BUILDDIR      = _build
GH_PAGES_SOURCES = . Makefile

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile livehtml

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

# This was stolen from:
# http://nikhilism.com/post/2012/automatic-github-pages-generation-from/
gh-pages:
	git checkout gh-pages
	rm -rf _build _sources _static
	git checkout develop $(GH_PAGES_SOURCES)
	git reset HEAD
	make html
	mv -fv _build/html/* ./
	rm -rf $(GH_PAGES_SOURCES) _build
	git add -A
	git ci -m "Generated gh-pages for `git log master -1 --pretty=short --abbrev-commit`" && git push origin gh-pages ; git checkout develop

livehtml: html
	livereload $(BUILDDIR)/html
