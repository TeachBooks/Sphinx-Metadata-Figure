extensions = [
    "sphinx_metadata_figure",
    "sphinxcontrib.bibtex",
]

bibtex_bibfiles = ["existing.bib"]
bibtex_default_style = "unsrt"

metadata_figure_settings = {
    "style": {
        "placement": "caption",
        "show": "author,license,date",
    },
    "bib": {
        "extract_metadata": True,
        "generate_bib": True,
        "output_file": "_generated_figures.bib",
    },
}

project = "BibTest"
master_doc = "index"
exclude_patterns = ["_build"]
