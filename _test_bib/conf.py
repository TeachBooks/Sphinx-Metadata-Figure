extensions = [
    "sphinx_metadata_figure",
    "sphinxcontrib.bibtex",
]

bibtex_bibfiles = ["existing.bib"]
bibtex_default_style = "unsrt"

project = "Full Test"
author = "Config Author"
copyright = "2024 Config Copyright"

metadata_figure_settings = {
    "style": {
        "placement": "caption",
        "show": "author,license,date,copyright,source",
    },
    "license": {
        "substitute_missing": False,
        "individual": True,
    },
    "author": {
        "substitute_missing": True,
        "default_author": "config",
    },
    "date": {
        "substitute_missing": True,
        "default_date": "2025-01-01",
    },
    "copyright": {
        "substitute_missing": True,
        "default_copyright": "authoryear",
    },
    "source": {
        "warn_missing": False,
    },
    "bib": {
        "extract_metadata": True,
        "generate_bib": True,
        "output_file": "_generated_figures.bib",
    },
}

master_doc = "index"
exclude_patterns = ["_build"]
