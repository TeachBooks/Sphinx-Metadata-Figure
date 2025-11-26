"""
Sphinx Configuration File
==========================

Configuration file for Sphinx documentation builder with custom figure directive.
"""

import sys
from pathlib import Path

# -- Path setup --------------------------------------------------------------

# Add custom extension directory to Python path
sys.path.insert(0, str(Path('_ext').resolve()))

# -- Project information -----------------------------------------------------

project = 'Custom Figure Documentation'
copyright = '2025 TU Delft'
author = 'Dummy Author'

# The full version, including alpha/beta/rc tags
release = '0.1.0'

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings
extensions = [
    'myst_parser',        # MyST Markdown parser
    'sphinx_metadata_figure',      # Our custom figure directive
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
]

# MyST-Parser configuration
myst_enable_extensions = [
    "colon_fence",      # Enable ::: fences
    "deflist",          # Definition lists
    "tasklist",         # Task lists
    "fieldlist",        # Field lists
    "attrs_inline",     # Inline attributes
    "attrs_block",      # Block attributes
]

# Add any paths that contain templates here, relative to this directory
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files
exclude_patterns = [
    '_build',
    'Thumbs.db',
    '.DS_Store',
    '.venv',
    '.venv/**',
    'venv',
    'venv/**',
    '**/site-packages/**',
    '**/*.dist-info/**',
]

# The suffix(es) of source filenames
source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}

# The master document
master_doc = 'index'

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages
html_theme = 'alabaster'

# Add any paths that contain custom static files (such as style sheets)
html_static_path = ['_static']

# Custom CSS files (extension already injects custom_figure.css)
html_css_files = []

# Theme options
html_theme_options = {
    'description': 'Documentation with enhanced figure metadata',
    'github_user': 'your-username',
    'github_repo': 'your-repo',
}

# -- Options for LaTeX output ------------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper')
    'papersize': 'letterpaper',
    
    # The font size ('10pt', '11pt' or '12pt')
    'pointsize': '10pt',
}

# -- Extension configuration -------------------------------------------------

metadata_figure_settings = dict({
    # 'style': {
        # 'placement': 'caption',  # caption | admonition | margin
        # 'show': 'author,license,date',     # which fields to display
        # 'admonition_title': 'Attribution',            # title for the admonition block
        # 'admonition_class': 'attribution', # extra CSS class on the admonition
    # },
    # 'license': {
        # 'link_license'       : False,
        # 'strict_check'       : True,
        # 'summaries'          : False,
        # 'individual'         : False,
        # 'substitute_missing' : True,
        # 'default_license'    : 'CC-BY-SA'
    # },
    # 'author': {
    #     'substitute_missing' : True,
        # 'default_author'     : 'That is me'  # use 'config' to pull from Sphinx config author
    # },
    # 'date': {
    #     'substitute_missing' : True,
    #     'default_date'       : '2031-10-21'   # use 'today' for current date
    # },
    # 'copyright': {
    #     'substitute_missing': True,
    #     'default_copyright': 'config-authoryear'  # 'authoryear' | 'config' | 'authoryear-config' | 'config-authoryear' | 'anything else'
    # }
    'source': {
        'warn_missing' : True
    }
})