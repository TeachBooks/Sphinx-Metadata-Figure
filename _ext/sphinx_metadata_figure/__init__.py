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

from docutils import nodes
from docutils.parsers.rst import directives
from sphinx.directives.patches import Figure
from sphinx.util import logging
from datetime import datetime

from sphinx.locale import get_translation
MESSAGE_CATALOG_NAME = "sphinx_metadata_figure"
translate = get_translation(MESSAGE_CATALOG_NAME)

logger = logging.getLogger(__name__)

# List of valid licenses
VALID_LICENSES = [
    'CC0',
    'CC-BY',
    'CC-BY-SA',
    'CC-BY-NC',
    'CC-BY-NC-SA',
    'CC-BY-ND',
    'CC-BY-NC-ND',
    'Public Domain',
    'MIT',
    'Apache-2.0',
    'GPL-3.0',
    'BSD-3-Clause',
    'Proprietary',
    'All Rights Reserved',
    'Pixabay License',
    'Unsplash License',
    'Pexels License',
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
    'Public Domain': 'https://creativecommons.org/publicdomain/mark/1.0/',
    'MIT': 'https://opensource.org/licenses/MIT',
    'Apache-2.0': 'https://www.apache.org/licenses/LICENSE-2.0',
    'GPL-3.0': 'https://www.gnu.org/licenses/gpl-3.0.en.html',
    'BSD-3-Clause': 'https://opensource.org/licenses/BSD-3-Clause',
    'Pixabay License': 'https://pixabay.com/service/terms/#license',
    'Unsplash License': 'https://unsplash.com/license',
    'Pexels License': 'https://www.pexels.com/license/',
}

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
        # New options for display/behavior
        'placement': directives.unchanged,          # caption | admonition | margin
        'show': directives.unchanged,               # comma-separated: author,license,date
        'title': directives.unchanged,              # admonition title (default: Attribution)
        'admonition_class': directives.unchanged,   # extra classes for admonition
    })

    def run(self):
        """
        Process the directive and validate metadata.
        
        Returns:
            list: List of docutils nodes to be inserted into the document
        """
        # Validate license
        license_value = self.options.get('license', None)
        
        if license_value is None:
            # Warn if license is missing
            logger.warning(
                f'\n- Figure "{self.arguments[0]}" '
                f'is missing license information.\n'
                f'- Please add the :license: option with a recognized license.\n'
                f'- Recognized licenses: {", ".join(VALID_LICENSES)}',
                location=(self.state.document.current_source, self.lineno)
            )
        elif license_value not in VALID_LICENSES:
            # Warn if license is invalid
            logger.warning(
                f'\n- Figure "{self.arguments[0]}" '
                f'has an unrecognized license "{license_value}".\n'
                f'- Recognized licenses: {", ".join(VALID_LICENSES)}',
                location=(self.state.document.current_source, self.lineno)
            )
        
        # Validate date format (optional)
        date_value = self.options.get('date', None)
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
        
        # Generate the base figure nodes using parent class
        figure_nodes = super().run()

        # Access environment/config for defaults and per-file metadata
        env = getattr(self.state.document.settings, 'env', None)
        config = getattr(env.app, 'config', None) if env else None

        # Resolve effective values (option -> doc meta -> global defaults)
        doc_meta = {}
        if env:
            meta = env.metadata.get(env.docname, {})
            # Support both tb_attribution_* and attribution_* keys
            def _m(key):
                return (
                    meta.get(f'tb_attribution_{key}')
                    or meta.get(f'attribution_{key}')
                    or meta.get(key)
                )
            # Values may be list-like; coerce to scalar if needed
            def _coerce(v):
                if isinstance(v, (list, tuple)):
                    return v[0] if v else None
                return v
            doc_meta = {
                'author': _coerce(_m('author')),
                'license': _coerce(_m('license')),
                'date': _coerce(_m('date')),
                'placement': _coerce(_m('placement')),
                'show': _coerce(_m('show')),
                'title': _coerce(_m('title')),
                'admonition_class': _coerce(_m('admonition_class')),
            }

        defaults = getattr(config, 'tb_attribution_defaults', {}) if config else {}

        def _resolve(name, opt_key=None):
            key = opt_key or name
            return (
                self.options.get(key)
                or doc_meta.get(name)
                or defaults.get(name)
            )

        # Effective metadata values
        author_value = _resolve('author')
        license_value = _resolve('license')
        date_value = _resolve('date')

        # Store metadata on the figure node, so builders can access it
        if figure_nodes:
            figure_node = figure_nodes[0]
            if author_value:
                figure_node['author'] = author_value
            if license_value:
                figure_node['license'] = license_value
            if date_value:
                figure_node['date'] = date_value

            # Determine rendering controls
            placement = (_resolve('placement') or 'caption').strip().lower()
            show_raw = _resolve('show') or 'author,license,date'
            show = [s.strip().lower() for s in str(show_raw).split(',') if s.strip()]
            title = _resolve('title') or 'Attribution'
            admon_class = _resolve('admonition_class') or 'attribution'

            display_nodes = self._build_attribution_display(
                figure_node=figure_node,
                placement=placement,
                show=show,
                title=title,
                admonition_class=admon_class,
                link_license=getattr(config, 'tb_attribution_link_license', True) if config else True,
                license_urls=getattr(config, 'tb_attribution_license_urls', LICENSE_URLS) if config else LICENSE_URLS,
            )

            # Attach display according to placement
            if display_nodes:
                if placement == 'caption':
                    # paragraph node already targeted to append into figure
                    for n in display_nodes:
                        if isinstance(n, nodes.paragraph):
                            figure_node.append(n)
                        else:
                            figure_nodes.append(n)
                else:
                    figure_nodes.extend(display_nodes)

        return figure_nodes
    
    def _build_attribution_display(self, figure_node, placement, show, title,
                                   admonition_class, link_license, license_urls):
        """Create nodes to display attribution based on placement.

        Returns a list of nodes to append to the document. For placement='caption',
        the returned list will include a paragraph intended to be appended inside
        the figure node.
        """
        Add metadata display to the figure.
        
        Creates a paragraph with formatted metadata information that appears
        below the figure caption.
        
        Args:
            figure_node: The figure node to add metadata to
        """
        metadata_parts = []
        
        # Collect metadata parts
        if 'author' in figure_node:
            metadata_parts.append(f"{translate('Author')}: {figure_node['author']}")
        if 'license' in figure_node:
            metadata_parts.append(f"{translate('License')}: {figure_node['license']}")
        if 'date' in figure_node:
            metadata_parts.append(f"{translate('Date')}: {figure_node['date']}")
        
        # Add metadata paragraph if we have any metadata
        if metadata_parts:
            metadata_text = ' | '.join(metadata_parts)
            metadata_para = nodes.paragraph(
                text=metadata_text,
                classes=['figure-metadata']
            )
            figure_node.append(metadata_para)

        if not parts:
            return []

        text = ' | '.join(parts)

        if placement == 'caption':
            para = nodes.paragraph(text=text, classes=['figure-metadata', 'tb-attribution'])
            return [para]

        # Build an admonition-like block for other placements
        admon = nodes.admonition(classes=['tb-attribution', admonition_class])
        # Title
        admon += nodes.title(text=title)
        # Body paragraph
        body_para = nodes.paragraph(text=text)
        admon += body_para

        if placement == 'margin':
            # Add margin class to allow themes to style it in the margin
            admon['classes'].append('margin')
            admon['classes'].append('tb-margin')

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


def setup(app):
    """
    Setup function for the Sphinx extension.
    
    This function is called by Sphinx to register the extension.
    
    Args:
        app: Sphinx application instance
        
    Returns:
        dict: Extension metadata
    """
    # Register config values for global defaults and linking behavior
    app.add_config_value('tb_attribution_defaults', {}, 'env')
    app.add_config_value('tb_attribution_license_urls', LICENSE_URLS, 'env')
    app.add_config_value('tb_attribution_link_license', True, 'env')

    # Override the default figure directive with our custom version
    app.add_directive('figure', MetadataFigure, override=True)
    
    # Add custom CSS for metadata styling
    app.add_css_file('custom_figure.css')
    
    # Register event handler to check all figures after build
    app.connect('env-updated', check_all_figures_have_license)

    # add translations
    package_dir = os.path.abspath(os.path.dirname(__file__))
    locale_dir = os.path.join(package_dir, "translations", "locales")
    app.add_message_catalog(MESSAGE_CATALOG_NAME, locale_dir)
    
    return {
        'version': '0.1.0',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
