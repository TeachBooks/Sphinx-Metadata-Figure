"""
Custom Figure Directive Extension for Sphinx
==============================================

This extension extends the standard Sphinx figure directive to include:
- author: Author/creator of the image
- license: Image license (validated against a predefined list)
- date: Creation date (format: YYYY-MM-DD)

During parsing, it validates that all images have proper and recognized license information.
"""

import os
import json

from docutils import nodes
from docutils.parsers.rst import directives
from sphinx.directives.patches import Figure
from sphinx.util import logging
from datetime import datetime
from sphinx.util.fileutil import copy_asset
from pathlib import Path
from sphinx.application import Sphinx
from typing import Union
from myst_nb.ext.glue.directives import PasteFigureDirective
from sphinx.util.docutils import SphinxDirective

from sphinx.writers.html import HTMLTranslator

from sphinx.locale import get_translation
MESSAGE_CATALOG_NAME = "sphinx_metadata_figure"
translate = get_translation(MESSAGE_CATALOG_NAME)

logger = logging.getLogger(__name__)

# Global defaults for figure attribution (can be overridden per file or per directive)
METADATA_FIGURE_DEFAULTS_STYLE = {
    'placement': 'hide',  # caption | admonition | margin | hide
    'show': 'author,license,date,copyright,source',     # which fields to display
    'admonition_title': 'Attribution',            # title for the admonition block
    'admonition_class': 'attribution', # extra CSS class on the admonition
}
METADATA_FIGURE_DEFAULTS_LICENSE = {
    'link_license'       : True,
    'strict_check'       : False,
    'summaries'          : False,
    'individual'         : False,
    'substitute_missing' : False,
    'default_license'    : 'CC BY'
}
METADATA_FIGURE_DEFAULTS_AUTHOR = {
    'substitute_missing' : False,
    'default_author'     : 'config'  # use 'config' to pull from Sphinx config author
}
METADATA_FIGURE_DEFAULTS_DATE = {
    'substitute_missing' : False,
    'default_date'       : 'today'   # use 'today' for current date
}
METADATA_FIGURE_DEFAULTS_COPYRIGHT = {
    'substitute_missing' : False,
    'default_copyright'    : 'authoryear'  # 'authoryear' | 'config' | 'authoryear-config' | 'config-authoryear' | 'anything else'
}
METADATA_FIGURE_DEFAULTS_SOURCE = {
    'warn_missing' : False
}
METADATA_FIGURE_DEFAULTS_BIB = {
    'extract_metadata': True,    # Extract metadata from bib entries when :bib: is specified
    'generate_bib': False,       # Generate BibTeX entries from figure metadata
    'output_file': 'references.bib',  # Output file for generated BibTeX entries
    'overwrite_existing': False, # Whether to overwrite existing entries with the same key
}
METADATA_FIGURE_DEFAULTS = {
    'style': METADATA_FIGURE_DEFAULTS_STYLE,
    'license': METADATA_FIGURE_DEFAULTS_LICENSE,
    'author': METADATA_FIGURE_DEFAULTS_AUTHOR,
    'date': METADATA_FIGURE_DEFAULTS_DATE,
    'copyright': METADATA_FIGURE_DEFAULTS_COPYRIGHT,
    'source': METADATA_FIGURE_DEFAULTS_SOURCE,
    'bib': METADATA_FIGURE_DEFAULTS_BIB,
}

# List of valid licenses
VALID_LICENSES = [
    'CC0',
    'CC-BY',
    'CC-BY-SA',
    'CC-BY-NC',
    'CC-BY-NC-SA',
    'CC-BY-ND',
    'CC-BY-NC-ND',
    'CC BY',
    'CC BY-SA',
    'CC BY-NC',
    'CC BY-NC-SA',
    'CC BY-ND',
    'CC BY-NC-ND',
    'CC BY 4.0',
    'CC BY-SA 4.0',
    'CC BY-NC 4.0',
    'CC BY-NC-SA 4.0',
    'CC BY-ND 4.0',
    'CC BY-NC-ND 4.0',
    'CC BY 3.0',
    'CC BY-SA 3.0',
    'CC BY-NC 3.0',
    'CC BY-NC-SA 3.0',
    'CC BY-ND 3.0',
    'CC BY-NC-ND 3.0',
    "CC BY 2.5",
    "CC BY-SA 2.5",
    "CC BY-NC 2.5",
    "CC BY-NC-SA 2.5",
    "CC BY-ND 2.5",
    "CC BY-NC-ND 2.5",
    'CC BY 2.0',
    'CC BY-SA 2.0',
    'CC BY-NC 2.0',
    'CC BY-NC-SA 2.0',
    'CC BY-ND 2.0',
    'CC BY-NC-ND 2.0',
    'CC BY 1.0',
    'CC BY-SA 1.0',
    'CC BY-NC 1.0',
    'CC BY-NC-SA 1.0',
    'CC BY-ND 1.0',
    'CC BY-NC-ND 1.0',
    'Public Domain',
    'MIT',
    'Apache-2.0',
    'GPL-3.0',
    'BSD-3-Clause',
    'Proprietary',
    'All Rights Reserved',
    'Pixabay License',
    'Unsplash License',
    'Pexels License'
]

# Map known license tokens to canonical URLs (used when linking licenses)
LICENSE_URLS = {
    'CC0': 'https://creativecommons.org/publicdomain/zero/1.0/',
    'CC-BY': 'https://creativecommons.org/licenses/by/4.0/',
    'CC-BY-SA': 'https://creativecommons.org/licenses/by-sa/4.0/',
    'CC-BY-NC': 'https://creativecommons.org/licenses/by-nc/4.0/',
    'CC-BY-NC-SA': 'https://creativecommons.org/licenses/by-nc-sa/4.0/',
    'CC-BY-ND': 'https://creativecommons.org/licenses/by-nd/4.0/',
    'CC-BY-NC-ND': 'https://creativecommons.org/licenses/by-nc-nd/4.0/',
    'CC BY': 'https://creativecommons.org/licenses/by/4.0/',
    'CC BY-SA': 'https://creativecommons.org/licenses/by-sa/4.0/',
    'CC BY-NC': 'https://creativecommons.org/licenses/by-nc/4.0/',
    'CC BY-NC-SA': 'https://creativecommons.org/licenses/by-nc-sa/4.0/',
    'CC BY-ND': 'https://creativecommons.org/licenses/by-nd/4.0/',
    'CC BY-NC-ND': 'https://creativecommons.org/licenses/by-nc-nd/4.0/',
    'CC BY 4.0': 'https://creativecommons.org/licenses/by/4.0/',
    'CC BY-SA 4.0': 'https://creativecommons.org/licenses/by-sa/4.0/',
    'CC BY-NC 4.0': 'https://creativecommons.org/licenses/by-nc/4.0/',
    'CC BY-NC-SA 4.0': 'https://creativecommons.org/licenses/by-nc-sa/4.0/',
    'CC BY-ND 4.0': 'https://creativecommons.org/licenses/by-nd/4.0/',
    'CC BY-NC-ND 4.0': 'https://creativecommons.org/licenses/by-nc-nd/4.0/',
    'CC BY 3.0': 'https://creativecommons.org/licenses/by/3.0/',
    'CC BY-SA 3.0': 'https://creativecommons.org/licenses/by-sa/3.0/',
    'CC BY-NC 3.0': 'https://creativecommons.org/licenses/by-nc/3.0/',
    'CC BY-NC-SA 3.0': 'https://creativecommons.org/licenses/by-nc-sa/3.0/',
    'CC BY-ND 3.0': 'https://creativecommons.org/licenses/by-nd/3.0/',
    'CC BY-NC-ND 3.0': 'https://creativecommons.org/licenses/by-nc-nd/3.0/',
    "CC BY 2.5": "https://creativecommons.org/licenses/by/2.5/",
    "CC BY-SA 2.5": "https://creativecommons.org/licenses/by-sa/2.5/",
    "CC BY-NC 2.5": "https://creativecommons.org/licenses/by-nc/2.5/",
    "CC BY-NC-SA 2.5": "https://creativecommons.org/licenses/by-nc-sa/2.5/",
    "CC BY-ND 2.5": "https://creativecommons.org/licenses/by-nd/2.5/",
    "CC BY-NC-ND 2.5": "https://creativecommons.org/licenses/by-nc-nd/2.5/",
    'CC BY 2.0': 'https://creativecommons.org/licenses/by/2.0/',
    'CC BY-SA 2.0': 'https://creativecommons.org/licenses/by-sa/2.0/',
    'CC BY-NC 2.0': 'https://creativecommons.org/licenses/by-nc/2.0/',
    'CC BY-NC-SA 2.0': 'https://creativecommons.org/licenses/by-nc-sa/2.0/',
    'CC BY-ND 2.0': 'https://creativecommons.org/licenses/by-nd/2.0/',
    'CC BY-NC-ND 2.0': 'https://creativecommons.org/licenses/by-nc-nd/2.0/',
    'CC BY 1.0': 'https://creativecommons.org/licenses/by/1.0/',
    'CC BY-SA 1.0': 'https://creativecommons.org/licenses/by-sa/1.0/',
    'CC BY-NC 1.0': 'https://creativecommons.org/licenses/by-nc/1.0/',
    'CC BY-NC-SA 1.0': 'https://creativecommons.org/licenses/by-nc-sa/1.0/',
    'CC BY-ND 1.0': 'https://creativecommons.org/licenses/by-nd/1.0/',
    'CC BY-NC-ND 1.0': 'https://creativecommons.org/licenses/by-nc-nd/1.0/',
    'Public Domain': 'https://creativecommons.org/publicdomain/mark/1.0/',
    'MIT': 'https://opensource.org/licenses/MIT',
    'Apache-2.0': 'https://www.apache.org/licenses/LICENSE-2.0',
    'GPL-3.0': 'https://www.gnu.org/licenses/gpl-3.0.en.html',
    "GPL-2.0": "https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html",
    "LGPL-2.1": "https://www.gnu.org/licenses/lgpl-2.1.en.html",
    "LGPL-3.0": "https://www.gnu.org/licenses/lgpl-3.0.en.html",
    "AGPL-3.0": "https://www.gnu.org/licenses/agpl-3.0.en.html",
    'BSD-3-Clause': 'https://opensource.org/licenses/BSD-3-Clause',
    "BSD-2-Clause": "https://opensource.org/licenses/BSD-2-Clause",
    'Pixabay License': 'https://pixabay.com/service/terms/#license',
    'Unsplash License': 'https://unsplash.com/license',
    'Pexels License': 'https://www.pexels.com/license/'
}

def _strip_surrounding_braces(s: str) -> str:
    """
    Remove all braces from a BibTeX field value for display.
    
    BibTeX uses braces for two purposes:
    1. Delimiting field values: author = {value}
    2. Protecting text from case changes: {van} in names
    
    When displaying values, both types of braces should be removed.
    This function strips all braces while preserving the text content.
    
    Examples:
        "{{Some Author}}" -> "Some Author"
        "{Some Author}" -> "Some Author"  
        "John {van} Doe" -> "John van Doe" (inner braces removed too)
        "{John {van} Doe}" -> "John van Doe" (all braces removed)
    
    Manual test: Add a .bib entry with author = {John {van} Doe} and reference
    it with :bib: in a figure; the caption should render "John van Doe" (no braces).
    
    Args:
        s: The BibTeX field value to process
        
    Returns:
        The value with all braces removed
    """
    if not s:
        return s
    
    # Remove all braces (both { and })
    result = s.replace('{', '').replace('}', '')
    
    # Clean up any extra whitespace that might result from brace removal
    # Replace multiple spaces with single space and strip
    result = ' '.join(result.split())
    
    return result


def _parse_bib_entry(bib_content, key):
    """
    Parse a BibTeX entry and extract metadata fields.

    Args:
        bib_content: The full content of a .bib file
        key: The BibTeX key to look up

    Returns:
        dict: Extracted metadata or None if not found
    """
    import re

    # Find the entry with the given key
    # Pattern matches @type{key, ... }
    pattern = rf'@\w+\s*\{{\s*{re.escape(key)}\s*,([^@]*?)\}}\s*(?=@|\Z)'
    match = re.search(pattern, bib_content, re.DOTALL | re.IGNORECASE)

    if not match:
        return None

    entry_content = match.group(1)
    metadata = {}

    # Extract fields - pattern matches field = {value} or field = "value"
    field_pattern = r'(\w+)\s*=\s*(?:\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}|"([^"]*)")'

    for field_match in re.finditer(field_pattern, entry_content, re.DOTALL):
        field_name = field_match.group(1).lower()
        field_value = field_match.group(2) or field_match.group(3)
        if field_value:
            field_value = field_value.strip()
        if field_name == 'author':
            metadata['author'] = _strip_surrounding_braces(field_value)
        elif field_name == 'year':
            # Convert year to date format
            if 'date' not in metadata:
                metadata['date'] = f'{field_value}-01-01'
        elif field_name == 'date':
            metadata['date'] = field_value
        elif field_name == 'url':
            metadata['source'] = field_value
        elif field_name == 'howpublished':
            # Extract URL from \url{...} if present
            url_match = re.search(r'\\url\{([^}]+)\}', field_value)
            if url_match:
                metadata['source'] = url_match.group(1)
            elif 'source' not in metadata:
                metadata['source'] = field_value
        elif field_name == 'note':
            # Try to extract license from note field
            license_match = re.search(r'License:\s*(.+)', field_value, re.IGNORECASE)
            if license_match:
                metadata['license'] = license_match.group(1).strip()
        elif field_name == 'copyright':
            metadata['copyright'] = field_value

    return metadata if metadata else None


def _load_bib_files(app):
    """
    Load all .bib files configured in sphinxcontrib-bibtex or in source directory.

    Returns:
        str: Combined content of all bib files
    """
    bib_content = ''

    # Try to get bib files from sphinxcontrib-bibtex configuration
    bibtex_files = getattr(app.config, 'bibtex_bibfiles', [])

    # Also search for .bib files in the source directory
    srcdir = app.srcdir
    for bib_file in bibtex_files:
        bib_path = os.path.join(srcdir, bib_file)
        if os.path.exists(bib_path):
            try:
                with open(bib_path, 'r', encoding='utf-8') as f:
                    bib_content += f.read() + '\n'
            except Exception as e:
                logger.debug(f'Could not read bib file {bib_path}: {e}')

    # Search for any .bib files in source directory if none configured
    if not bib_content:
        for root, dirs, files in os.walk(srcdir):
            for file in files:
                if file.endswith('.bib'):
                    bib_path = os.path.join(root, file)
                    try:
                        with open(bib_path, 'r', encoding='utf-8') as f:
                            bib_content += f.read() + '\n'
                    except Exception as e:
                        logger.debug(f'Could not read bib file {bib_path}: {e}')

    return bib_content


def _generate_bib_entry(key, metadata, image_path, caption=None):
    """
    Generate a BibTeX entry from figure metadata.

    Args:
        key: BibTeX key for the entry
        metadata: dict containing figure metadata (author, license, date, copyright, source)
        image_path: Path to the image file
        caption: Optional figure caption

    Returns:
        str: Formatted BibTeX entry
    """
    import re

    # Start with @misc entry type (most appropriate for figures/images)
    bib_lines = [f'@misc{{{key},']

    # Add author if present
    if metadata.get('author'):
        bib_lines.append(f'  author = {{{metadata["author"]}}},')

    # Add title (use caption or image filename)
    if caption:
        title = caption.strip()
    else:
        title = f'Figure: {image_path}'
    bib_lines.append(f'  title = {{{title}}},')

    # Add date/year
    if metadata.get('date'):
        date_str = metadata['date']
        # Extract year from date if in YYYY-MM-DD format
        try:
            year = datetime.strptime(date_str, '%Y-%m-%d').year
            bib_lines.append(f'  year = {{{year}}},')
            bib_lines.append(f'  date = {{{date_str}}},')
        except ValueError:
            # If date is not in expected format, just use it as-is
            bib_lines.append(f'  year = {{{date_str}}},')

    # Add source as URL or howpublished
    if metadata.get('source'):
        source = metadata['source']
        # Check if it's a URL
        if source.startswith('http://') or source.startswith('https://'):
            bib_lines.append(f'  url = {{{source}}},')
            bib_lines.append(f'  howpublished = {{\\url{{{source}}}}},')
        elif source.startswith('[') and '](' in source:
            # Markdown link format: [text](url)
            match = re.match(r'\[([^\]]+)\]\(([^\)]+)\)', source)
            if match:
                url = match.group(2)
                bib_lines.append(f'  url = {{{url}}},')
                bib_lines.append(f'  howpublished = {{\\url{{{url}}}}},')
        else:
            bib_lines.append(f'  howpublished = {{{source}}},')

    # Add license in note field
    if metadata.get('license'):
        bib_lines.append(f'  note = {{License: {metadata["license"]}}},')

    # Add copyright
    if metadata.get('copyright'):
        bib_lines.append(f'  copyright = {{{metadata["copyright"]}}},')

    # Close the entry
    bib_lines.append('}')

    return '\n'.join(bib_lines)


def _inject_into_bibtex_cache(app, bib_key, metadata, image_path, caption=None):
    """
    Inject a generated BibTeX entry directly into sphinxcontrib-bibtex's cache.

    This allows the entry to be cited in the same build without requiring a rebuild.

    Args:
        app: Sphinx application instance
        bib_key: The BibTeX key for the entry
        metadata: dict containing figure metadata
        image_path: Path to the image file
        caption: Optional figure caption

    Returns:
        bool: True if injection succeeded, False otherwise
    """
    try:
        # Import pybtex for creating Entry objects
        from pybtex.database import Entry, Person

        # Access sphinxcontrib-bibtex's cache
        env = app.env
        if not hasattr(env, 'bibtex_bibfiles'):
            logger.debug('sphinxcontrib-bibtex cache not found (bibtex_bibfiles)')
            return False

        bibfiles = env.bibtex_bibfiles
        if not bibfiles:
            logger.debug('No bibfiles in sphinxcontrib-bibtex cache')
            return False

        # Build entry fields
        fields = {}

        # Title
        if caption:
            fields['title'] = caption.strip()
        else:
            fields['title'] = f'Figure: {image_path}'

        # Date/Year
        if metadata.get('date'):
            date_str = metadata['date']
            try:
                year = datetime.strptime(date_str, '%Y-%m-%d').year
                fields['year'] = str(year)
                fields['date'] = date_str
            except ValueError:
                fields['year'] = date_str

        # Source
        if metadata.get('source'):
            source = metadata['source']
            if source.startswith('http://') or source.startswith('https://'):
                fields['url'] = source
                fields['howpublished'] = f'\\url{{{source}}}'
            elif source.startswith('[') and '](' in source:
                import re
                match = re.match(r'\[([^\]]+)\]\(([^\)]+)\)', source)
                if match:
                    url = match.group(2)
                    fields['url'] = url
                    fields['howpublished'] = f'\\url{{{url}}}'
            else:
                fields['howpublished'] = source

        # License in note
        if metadata.get('license'):
            fields['note'] = f'License: {metadata["license"]}'

        # Copyright
        if metadata.get('copyright'):
            fields['copyright'] = metadata['copyright']

        # Create pybtex Entry
        entry = Entry('misc', fields=fields)

        # Handle author separately (pybtex uses Person objects)
        if metadata.get('author'):
            author_str = metadata['author']
            # Simple parsing - split by 'and' for multiple authors
            author_parts = [a.strip() for a in author_str.split(' and ')]
            persons = []
            for author in author_parts:
                persons.append(Person(author))
            entry.persons['author'] = persons

        # Inject into the first available bibfile's data
        for bibfile_key, bibfile_data in bibfiles.items():
            if hasattr(bibfile_data, 'data') and hasattr(bibfile_data.data, 'entries'):
                # Check if key already exists
                if bib_key in bibfile_data.data.entries:
                    logger.debug(f'BibTeX key "{bib_key}" already exists in cache')
                    return True  # Already exists, consider it success

                bibfile_data.data.entries[bib_key] = entry
                logger.debug(f'Injected BibTeX entry "{bib_key}" into sphinxcontrib-bibtex cache')
                return True

        logger.debug('Could not find suitable bibfile data structure for injection')
        return False

    except ImportError:
        logger.debug('pybtex not available for cache injection')
        return False
    except Exception as e:
        logger.debug(f'Failed to inject into bibtex cache: {e}')
        return False


def _write_bib_entry(app, bib_key, bib_entry, output_file, overwrite=False):
    """
    Write a BibTeX entry to a file, avoiding duplicates.

    Args:
        app: Sphinx application instance
        bib_key: The BibTeX key
        bib_entry: The formatted BibTeX entry string
        output_file: Path to the output .bib file (relative to srcdir)
        overwrite: Whether to overwrite existing entries with the same key

    Returns:
        bool: True if write succeeded, False otherwise
    """
    import re

    # Resolve output path
    output_path = _resolve_bib_output_path(app, output_file)

    # Read existing content if file exists
    existing_content = ''
    if os.path.exists(output_path):
        try:
            with open(output_path, 'r', encoding='utf-8') as f:
                existing_content = f.read()
        except Exception as e:
            logger.warning(f'Could not read existing bib file {output_path}: {e}')
            return False

    # Check if entry with this key already exists
    pattern = rf'@\w+\s*\{{\s*{re.escape(bib_key)}\s*,'
    existing_match = re.search(pattern, existing_content, re.IGNORECASE)

    if existing_match:
        if not overwrite:
            logger.debug(f'BibTeX entry with key "{bib_key}" already exists in {output_path}, skipping')
            return True  # Not an error, just skipping
        else:
            # Remove the existing entry
            full_pattern = rf'@\w+\s*\{{\s*{re.escape(bib_key)}\s*,([^@]*?)\}}\s*(?=@|\Z)'
            existing_content = re.sub(full_pattern, '', existing_content, flags=re.DOTALL | re.IGNORECASE)
            logger.debug(f'Overwriting existing BibTeX entry with key "{bib_key}" in {output_path}')

    # Append new entry
    if existing_content and not existing_content.endswith('\n\n'):
        if existing_content.endswith('\n'):
            bib_entry = '\n' + bib_entry
        else:
            bib_entry = '\n\n' + bib_entry

    # Write to file
    try:
        # Ensure directory exists
        os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(existing_content + bib_entry + '\n')

        logger.info(f'Generated BibTeX entry for "{bib_key}" in {output_path}')
        return True
    except Exception as e:
        logger.warning(f'Could not write BibTeX entry to {output_path}: {e}')
        return False


class DefaultMetadataPage(SphinxDirective):
    """
    Set default metadata values for all figures on the current page.

    This directive allows you to set page-level defaults that apply to all figures
    in the current document. These defaults have lower priority than explicit figure
    options but higher priority than global configuration defaults.

    Example usage:
        .. default-metadata-page::
           :author: John Doe
           :license: CC-BY
           :placement: admonition
    """
    has_content = False
    required_arguments = 0
    option_spec = {
        'author': directives.unchanged,
        'license': directives.unchanged,
        'date': directives.unchanged,
        'copyright': directives.unchanged,
        'source': directives.unchanged,
        'placement': directives.unchanged,
        'show': directives.unchanged,
        'admonition_title': directives.unchanged,
        'admonition_class': directives.unchanged,
    }

    def run(self):
        """Store the page-level defaults in the environment."""
        env = self.state.document.settings.env

        # Initialize the page defaults dict if it doesn't exist
        if not hasattr(env, 'metadata_figure_page_defaults'):
            env.metadata_figure_page_defaults = {}

        # Store defaults for this document
        docname = env.docname
        env.metadata_figure_page_defaults[docname] = self.options.copy()

        # Return empty list - this directive doesn't produce visible output
        return []


class MetadataFigure(Figure):
    """
    Enhanced figure directive with metadata support.
    
    This directive extends the standard Sphinx figure directive by adding
    three new options:
    - author: The author/creator of the image
    - license: The license under which the image is distributed
    - date: The creation date of the image (YYYY-MM-DD format)
    """
    
    # Copy parent's option_spec and add our custom options
    option_spec = Figure.option_spec.copy()
    option_spec.update({
        'author': directives.unchanged,
        'license': directives.unchanged,
        'date': directives.unchanged,
        'copyright': directives.unchanged,
        'source': directives.unchanged,
        # New options for display/behavior
        'placement': directives.unchanged,          # caption | admonition | margin | hide
        'show': directives.unchanged,               # comma-separated: author,license,date
        'admonition_title': directives.unchanged,              # admonition title (default: Attribution)
        'admonition_class': directives.unchanged,   # extra classes for admonition
        # Bib entry support
        'bib': directives.unchanged,                # BibTeX key to use/generate for this figure
    })

    def run(self):
        """
        Process the directive and validate metadata.
        
        Returns:
            list: List of docutils nodes to be inserted into the document
        """

        # Access environment/config for defaults and per-file metadata
        env = getattr(self.state.document.settings, 'env', None)
        config = getattr(env.app, 'config', None) if env else None
        user_settings = getattr(config, 'metadata_figure_settings', {}) if config else {}

        # Deep merge: merge each category separately to preserve unspecified defaults
        settings = {}
        for key in METADATA_FIGURE_DEFAULTS:
            settings[key] = METADATA_FIGURE_DEFAULTS[key] | user_settings.get(key, {})

        # Retrieve page-level defaults if they exist
        page_defaults = {}
        if env and hasattr(env, 'metadata_figure_page_defaults'):
            docname = env.docname
            page_defaults = env.metadata_figure_page_defaults.get(docname, {})

        # Handle bib entry extraction - extract metadata from bib entry if :bib: is specified
        bib_key = self.options.get('bib', None)
        bib_settings = settings['bib']
        bib_metadata = {}

        # Check if an existing bibtex key is given
        if bib_key and bib_settings['extract_metadata'] and env:
            # Load bib files and try to extract metadata
            bib_content = _load_bib_files(env.app)
            if bib_content:
                extracted = _parse_bib_entry(bib_content, bib_key)
                if extracted:
                    bib_metadata = extracted
                    # add it to the bibliography
                    text = f"{{cite:empty}}`{bib_key}`"
                    para = nodes.paragraph()
                    self.state.nested_parse([text], self.content_offset, para)
                    # Add the paragraph node to the document
                    self.state.document += para
                else:
                    message_unrecognized = (
                        f'\n- Figure "{self.arguments[0]}" '
                            f'has an unrecognized BibTeX key "{bib_key}".'
                    )
                    logger.warning(
                        message_unrecognized,
                        location=(self.state.document.current_source, self.lineno)
                    )

        # Validate license (explicit option > bib metadata > page defaults > defaults)
        license_value = self.options.get('license', None) or bib_metadata.get('license', None) or page_defaults.get('license', None)
        license_settings = settings['license']
        if not license_value:
            if license_settings['substitute_missing']:
                license_value = license_settings['default_license']

        if license_value:
            license_value = untranslate_license(license_value)
        
        if license_value is None:
            # Warn or raise error if license is missing
            message_missing = (
                f'\n- Figure "{self.arguments[0]}" '
                f'is missing license information.\n'
                f'- Please add the :license: option with a recognized license.\n'
                f'- Recognized licenses: {", ".join(VALID_LICENSES)}'
            )
            if license_settings['strict_check']:
                raise ValueError(message_missing)
            elif license_settings['individual']:
                logger.warning(
                    message_missing,
                    location=(self.state.document.current_source, self.lineno)
                )
        elif license_value not in VALID_LICENSES:
            # Warn or raise error if license is invalid
            message_incorrect = (
                f'\n- Figure "{self.arguments[0]}" '
                    f'has an unrecognized license "{license_value}".\n'
                    f'- Recognized licenses: {", ".join(VALID_LICENSES)}'
            )
            if license_settings['strict_check']:
                raise ValueError(message_incorrect)
            elif license_settings['individual']:
                logger.warning(
                    message_incorrect,
                    location=(self.state.document.current_source, self.lineno)
            )
        # Translate the license, remove dashes in CC licenses and add version if missing for display
        if license_value:
            # translate:
            license_value = translate(license_value)
            # remove dashes in CC licenses for display
            if license_value.startswith("CC-"):
                license_value = license_value.replace("CC-", "CC ")
            # add 4.0 to CC licenses without version
            if license_value.startswith("CC ") and not any(char.isdigit() for char in license_value):
                license_value += " 4.0"
        
        # Validate date format (explicit option > bib metadata > page defaults > defaults)
        date_value = self.options.get('date', None) or bib_metadata.get('date', None) or page_defaults.get('date', None)
        if not date_value:
             date_settings = settings['date']
             if date_settings['substitute_missing']:
                date_value = date_settings['default_date']
        if date_value:
            if date_value == 'today':
                date_value = datetime.today().strftime('%Y-%m-%d')
        if date_value:
            try:
                datetime.strptime(date_value, '%Y-%m-%d')
            except ValueError:
                logger.warning(
                    f'Figure "{self.arguments[0]}" at '
                    f'{self.state.document.current_source}:{self.lineno} '
                    f'has invalid date format "{date_value}". '
                    f'Expected format: YYYY-MM-DD (e.g., 2025-01-15)',
                    location=(self.state.document.current_source, self.lineno)
                )

        # Author value (explicit option > bib metadata > page defaults > defaults)
        author_value = self.options.get('author', None) or bib_metadata.get('author', None) or page_defaults.get('author', None)
        if not author_value:
            author_settings = settings['author']
            if author_settings['substitute_missing']:
                default_author = author_settings['default_author']
                if default_author == 'config':
                    author_value = getattr(config, 'author', None)
                else:
                    author_value = default_author

        # Copyright value (explicit option > bib metadata > page defaults > defaults)
        copyright_value = self.options.get('copyright', None) or bib_metadata.get('copyright', None) or page_defaults.get('copyright', None)
        if not copyright_value:
            copyright_settings = settings['copyright']
            if copyright_settings['substitute_missing']:
                default_copyright = copyright_settings['default_copyright']
                if default_copyright == 'authoryear':
                    if author_value and date_value:
                        year =  datetime.strptime(date_value, "%Y-%m-%d").year
                        copyright_value = f'© {year} {author_value}'
                    elif author_value:
                        copyright_value = f'© {author_value}'
                    elif date_value:
                        year =  datetime.strptime(date_value, "%Y-%m-%d").year
                        copyright_value = f'© {year}'
                elif default_copyright == 'config':
                    if getattr(config, 'copyright', None):
                        copyright_value = getattr(config, 'copyright', None)
                elif default_copyright == 'authoryear-config':
                    if author_value and date_value:
                        year =  datetime.strptime(date_value, "%Y-%m-%d").year
                        copyright_value = f'© {year} {author_value}'
                    elif author_value:
                        copyright_value = f'© {author_value}'
                    elif date_value:
                        year =  datetime.strptime(date_value, "%Y-%m-%d").year
                        copyright_value = f'© {year}'
                    else:
                        if getattr(config, 'copyright', None):
                            copyright_value = getattr(config, 'copyright', None)
                elif default_copyright == 'config-authoryear':
                    if getattr(config, 'copyright', None):
                        copyright_value = getattr(config, 'copyright', None)
                    elif author_value and date_value:
                        year =  datetime.strptime(date_value, "%Y-%m-%d").year
                        copyright_value = f'© {year} {author_value}'
                    elif author_value:
                        copyright_value = f'© {author_value}'
                    elif date_value:
                        year =  datetime.strptime(date_value, "%Y-%m-%d").year
                        copyright_value = f'© {year}'
                else:
                    copyright_value = default_copyright
        
        # Source value (explicit option > bib metadata > page defaults)
        source_value = self.options.get('source', None) or bib_metadata.get('source', None) or page_defaults.get('source', None)
        source_settings = settings['source']
        if source_value is None:
            if source_settings['warn_missing']:
                # Warn if source is missing (if requested)
                message_missing = (
                    f'\n- Figure "{self.arguments[0]}" '
                    f'is missing source information.\n'
                    f'- Please add the :source: option with a source.'
                    f'- Either a URL (starting with "http" or "https"), a textual source description, or a MarkDown link.'
                )
                logger.warning(
                    message_missing,
                    location=(self.state.document.current_source, self.lineno)
                )
        if source_value == 'document':
            # Get the source file path relative to the source directory
            docname = env.docname if env else ''
            source_suffix = env.config.source_suffix if env and hasattr(env.config, 'source_suffix') else {'.rst': None, '.md': None}
            
            # Determine the actual source file extension
            source_file = None
            if isinstance(source_suffix, dict):
                for suffix in source_suffix.keys():
                    potential_path = env.doc2path(docname, base=False) if env else docname + suffix
                    if env and os.path.exists(os.path.join(env.srcdir, potential_path)):
                        source_file = potential_path
                        break
            
            if not source_file:
                source_file = env.doc2path(docname, base=False) if env else docname + '.rst'
            
            # Create absolute link to _sources directory where Sphinx copies source files
            source_link = f'/_sources/{source_file}'
            source_value = f'[Source code]({source_link})'
                
        # Generate the base figure nodes using parent class
        if self.name == 'glue:figure':
            temp = PasteFigureDirective(self.name, self.arguments, self.options,
                                        self.content, self.lineno, self.content_offset,
                                        self.block_text, self.state, self.state_machine)
            # Handle the myst_nb glue figure directive
            figure_nodes = PasteFigureDirective.run(temp)
        else:
            figure_nodes = Figure.run(self)
        # pretty print the node and stop here for debugging
        for node in figure_nodes:
            for child in node.children:
                has_caption = False
                if isinstance(child, nodes.caption):
                    has_caption = True
            node["unnumbered_caption"] = not has_caption
                # add a flag for adding an unnumbered caption later
                
                    
        # Store metadata on the figure node, so builders can access it
        if figure_nodes:
            figure_node = figure_nodes[0]
            if author_value:
                figure_node['author'] = author_value
            if license_value:
                figure_node['license'] = license_value
            if date_value:
                figure_node['date'] = date_value
            if copyright_value:
                figure_node['copyright'] = copyright_value
            if source_value:
                figure_node['source'] = source_value

            # Generate BibTeX entry if requested and key is specified but entry doesn't exist
            if bib_settings.get('generate_bib') and bib_key and env and not bib_metadata:
                # Collect metadata for BibTeX generation
                metadata_dict = {}
                if author_value:
                    metadata_dict['author'] = author_value
                if license_value:
                    metadata_dict['license'] = license_value
                if date_value:
                    metadata_dict['date'] = date_value
                if copyright_value:
                    metadata_dict['copyright'] = copyright_value
                if source_value:
                    metadata_dict['source'] = source_value

                # Extract caption from figure node
                caption_text = None
                for child in figure_node.children:
                    if isinstance(child, nodes.caption):
                        caption_text = child.astext()
                        break

                # Only generate if we have some metadata
                if metadata_dict:
                    image_path = self.arguments[0]
                    output_file = bib_settings.get('output_file', 'references.bib')
                    overwrite = bib_settings.get('overwrite_existing', False)

                    # Generate the BibTeX entry string
                    bib_entry = _generate_bib_entry(bib_key, metadata_dict, image_path, caption_text)

                    # 1. Try to inject into sphinxcontrib-bibtex cache (for same-build citation)
                    cache_injected = _inject_into_bibtex_cache(
                        env.app, bib_key, metadata_dict, image_path, caption_text
                    )

                    # 2. Write to .bib file (for persistence and future builds)
                    file_written = _write_bib_entry(env.app, bib_key, bib_entry, output_file, overwrite)

                    # 3. Add citation reference if cache injection succeeded
                    if cache_injected:
                        text = f"{{cite:empty}}`{bib_key}`"
                        para = nodes.paragraph()
                        self.state.nested_parse([text], self.content_offset, para)
                        self.state.document += para
                    elif file_written:
                        # Cache injection failed but file was written - warn about rebuild
                        logger.warning(
                            f'BibTeX entry "{bib_key}" generated but requires rebuild for citation. '
                            f'Run the build again to enable citations.',
                            location=(self.state.document.current_source, self.lineno)
                        )

            # Determine rendering controls (explicit option > page defaults > global config)
            style_settings = settings['style']
            placement = self.options.get('placement') or page_defaults.get('placement') or style_settings['placement']
            placement = placement.strip().lower()
            show_raw = self.options.get('show') or page_defaults.get('show') or style_settings['show']
            show = [s.strip().lower() for s in str(show_raw).split(',') if s.strip()]
            title = self.options.get('admonition_title') or page_defaults.get('admonition_title') or translate(style_settings['admonition_title'])
            admon_class = self.options.get('admonition_class') or page_defaults.get('admonition_class') or style_settings['admonition_class']
            
            display_nodes = _build_attribution_display(
                figure_node=figure_node,
                placement=placement,
                show=show,
                title=title,
                admonition_class=admon_class,
                link_license=license_settings.get('link_license', True) if config else True
            )

            # Attach display according to placement
            if display_nodes:
                if placement == 'caption':
                    # Append to caption (as raw HTML) so that is inserted during html rendering
                    figure_node['license_html'] = display_nodes
                elif placement == 'margin':
                    # Insert margin admonition before the figure so it appears next to it
                    figure_nodes = display_nodes + figure_nodes
                else:
                    # For 'admonition' placement, append after the figure
                    figure_nodes.extend(display_nodes)

        return figure_nodes
    
def _build_attribution_display(figure_node, placement, show, title,
                                admonition_class, link_license):
    """Create nodes to display attribution based on placement.

    Returns a list of nodes to append to the document. For placement='caption',
    the returned list will include a paragraph intended to be appended inside
    the figure node.
    """
    parts = []
    if placement == 'hide':
        return []
    if 'author' in figure_node and 'author' in show:
        parts.append((f"{translate('Author')}: {figure_node['author']}", None))
    if 'license' in figure_node and 'license' in show:
        if link_license and figure_node['license'] in LICENSE_URLS:
            license_url = LICENSE_URLS[figure_node['license']]
            parts.append((f"{translate('License')}: ", (figure_node['license'], license_url)))
        else:
            parts.append((f"{translate('License')}: {figure_node['license']}", None))
    if 'date' in figure_node and 'date' in show:
        parts.append((f"{translate('Date')}: {figure_node['date']}", None))
    if 'copyright' in figure_node and 'copyright' in show:
        parts.append((f"{translate('Copyright')}: {figure_node['copyright']}", None))
    if 'source' in figure_node and 'source' in show:
        if figure_node['source'].startswith('http'):
            parts.append((f"{translate('Source')}: ", (figure_node['source'], figure_node['source'])))
        elif len(figure_node['source'].split(']('))==2:
            # markdown link format: [text](url)
            text_part = figure_node['source'].split('](')[0].lstrip('[')
            url_part = figure_node['source'].split('](')[1].rstrip(')')
            parts.append((f"{translate('Source')}: ", (text_part, url_part)))
        else:
            parts.append((f"{translate('Source')}: {figure_node['source']}", None))

    if not parts:
        return []

    if placement == 'caption': # CSS figure-metadata class styles it appropriately
        license_html = "<span class=\"figure-metadata\">"
        for i, (text_part, link_info) in enumerate(parts):
            if i > 0:
                license_html += ' | '
            license_html += text_part
            if link_info:
                link_text, link_url = link_info
                license_html += f'<a href="{link_url}" target="_blank" rel="noopener">{link_text}</a>'
        license_html += "</span>"
        if not figure_node["unnumbered_caption"]:
            license_html = '<br>' + license_html
        return license_html

    # Build an admonition-like block for other placements
    # admonition classes define the style
    admon = nodes.admonition(classes=[admonition_class])
    # Title
    admon += nodes.title(text=title)
    # Body paragraph
    body_para = nodes.paragraph()
    for i, (text_part, link_info) in enumerate(parts):
        if i > 0:
            body_para += nodes.Text(' | ')
        body_para += nodes.Text(text_part)
        if link_info:
            link_text, link_url = link_info
            ref = nodes.reference('', link_text, refuri=link_url, internal=False)
            body_para += ref
    admon += body_para

    if placement == 'margin':
        # Add margin class to allow themes to style it in the margin
        admon['classes'].append('margin')

    return [admon]


def check_all_figures_have_license(app, env):
    """
    Check that all figures in the documentation have license information.
    
    This function is called after the environment is updated. It traverses
    all documents and checks each figure node for license information.
    
    Args:
        app: Sphinx application instance
        env: Sphinx build environment
    """

    # Only report if requested
    user_settings = getattr(app.config, 'metadata_figure_settings', {}) if app else {}
    
    # Deep merge: merge each category separately to preserve unspecified defaults
    settings = {}
    for key in METADATA_FIGURE_DEFAULTS:
        settings[key] = METADATA_FIGURE_DEFAULTS[key] | user_settings.get(key, {})
    
    license_settings = settings['license']
    if not license_settings['summaries']:
        return
    
    missing_licenses = []
    unrecognized_licenses = []

    for docname in env.found_docs:
        try:
            doctree = env.get_doctree(docname)
            for node in doctree.traverse(nodes.figure):
                # Find the image URI for better error messages
                image_uri = 'unknown'
                for image_node in node.traverse(nodes.image):
                    image_uri = image_node.get('uri', 'unknown')
                    break
                if 'license' not in node:
                    missing_licenses.append((docname, image_uri))
                else:
                    license_value = node['license']
                    if license_value not in VALID_LICENSES:
                        unrecognized_licenses.append((docname, image_uri))

        except Exception as e:
            # Skip documents that can't be loaded
            logger.debug(f'Could not check figures in {docname}: {e}')
    
    # Report all missing licenses
    if missing_licenses:
        logger.warning(
            f'Found {len(missing_licenses)} figure(s) without license information:'
        )
        for docname, image_uri in missing_licenses:
            logger.warning(f'  - {docname}: {image_uri}')

    # Report all unrecognized licenses
    if unrecognized_licenses:
        logger.warning(
            f'Found {len(unrecognized_licenses)} figure(s) with unrecognized license information:'
        )
        for docname, image_uri in unrecognized_licenses:
            logger.warning(f'  - {docname}: {image_uri}')

def _resolve_bib_output_path(app, output_file: str) -> str:
    """Resolve bib output path consistently against the source directory."""
    if os.path.isabs(output_file):
        return output_file
    return os.path.join(app.srcdir, output_file)

def setup(app):
    """
    Setup function for the Sphinx extension.
    
    This function is called by Sphinx to register the extension.
    
    Args:
        app: Sphinx application instance
        
    Returns:
        dict: Extension metadata
    """
    
    # Ensure MysST NB is loaded before this extension so the glue domain is registered
    app.setup_extension('myst_nb')

    # Register configuration values    
    app.add_config_value('metadata_figure_settings', {}, 'env')

    # Override the default figure directive with our custom version
    app.add_directive('figure', MetadataFigure, override=True)
    app.add_directive_to_domain('glue', 'figure', MetadataFigure, override=True)

    # Register the page-level default metadata directive
    app.add_directive('default-metadata-page', DefaultMetadataPage)

    # Add custom CSS for metadata styling
    app.add_css_file('metadata_figure.css')
    app.connect("build-finished", copy_asset_files)

    # Register event handler to check all figures after build
    app.connect('env-updated', check_all_figures_have_license)

    # add translations
    package_dir = os.path.abspath(os.path.dirname(__file__))
    locale_dir = os.path.join(package_dir, "translations", "locales")
    app.add_message_catalog(MESSAGE_CATALOG_NAME, locale_dir)

    # add captions to unnumbered figures
    app.connect('doctree-resolved', add_unnumbered_caption)
    
    return {
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }

def copy_asset_files(app: Sphinx, exc: Union[bool, Exception]):
    """Copies required assets for formatting in HTML"""
    static_path = (
        Path(__file__).parent.joinpath("assets", "metadata_figure.css").absolute()
    )
    asset_files = [str(static_path)]

    if exc is None:
        for path in asset_files:
            copy_asset(path, str(Path(app.outdir).joinpath("_static").absolute()))


original_visit = HTMLTranslator.visit_caption
original_depart = HTMLTranslator.depart_caption


def custom_visit_caption(self, node):
    # Call original visit logic
    original_visit(self, node)

    # Inject extra content after original caption rendering
    figure = node.parent
    license_html = figure.get('license_html', [])
    if license_html:
        node.append(nodes.raw('', license_html, format='html'))

def custom_depart_caption(self, node):
    # Call original depart logic
    original_depart(self, node)

# Override methods
HTMLTranslator.visit_caption = custom_visit_caption
HTMLTranslator.depart_caption = custom_depart_caption

def add_unnumbered_caption(app, doctree, fromdocname):
    """Add captions to unnumbered figures for metadata display."""
    for node in doctree.traverse(nodes.figure):
        has_caption = False
        has_license_html = 'license_html' in node
        if not has_license_html:
            continue
        for child in node.children:
            if isinstance(child, nodes.caption):
                has_caption = True
                break
        if not has_caption:
            if not node.get('ids'):
                env = app.builder.env
                serial = env.new_serialno('figure')
                node['ids'] = [nodes.make_id(f'figure-{serial}')]

            # add an empty caption so that metadata can be appended
            new_caption = nodes.caption(text="")
            node += new_caption

def untranslate_license(license_value: str) -> str:
    """Convert translated license names back to standard English keys."""
    """Independent of current locale."""

    # load untranslate map
    folder = os.path.abspath(os.path.dirname(__file__))
    locale_dir = os.path.join(folder, "translations", "untranslate.json")
    with open(locale_dir, 'r', encoding='utf-8') as f:
        untranslate_map = json.load(f)

    return untranslate_map.get(license_value, license_value)