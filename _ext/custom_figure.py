"""
Custom Figure Directive Extension for Sphinx
==============================================

This extension extends the standard Sphinx figure directive to include:
- author: Author/creator of the image
- license: Image license (validated against a predefined list)
- date: Creation date (format: YYYY-MM-DD)

During parsing, it validates that all images have proper license information.
"""

from docutils import nodes
from docutils.parsers.rst import directives
from sphinx.directives.patches import Figure
from sphinx.util import logging
from datetime import datetime

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
    'Pixabay License',
    'Unsplash License',
    'Pexels License',
]


class CustomFigure(Figure):
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
                f'Figure "{self.arguments[0]}" at '
                f'{self.state.document.current_source}:{self.lineno} '
                f'is missing license information. '
                f'Please add :license: option.',
                location=(self.state.document.current_source, self.lineno)
            )
        elif license_value not in VALID_LICENSES:
            # Warn if license is invalid
            logger.warning(
                f'Figure "{self.arguments[0]}" at '
                f'{self.state.document.current_source}:{self.lineno} '
                f'has invalid license "{license_value}". '
                f'Valid licenses: {", ".join(VALID_LICENSES)}',
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
        
        # Add metadata to the figure node
        if figure_nodes:
            figure_node = figure_nodes[0]
            
            # Store metadata as node attributes
            if 'author' in self.options:
                figure_node['author'] = self.options['author']
            if 'license' in self.options:
                figure_node['license'] = self.options['license']
            if 'date' in self.options:
                figure_node['date'] = self.options['date']
            
            # Optionally display metadata below the figure
            self._add_metadata_display(figure_node)
        
        return figure_nodes
    
    def _add_metadata_display(self, figure_node):
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
            metadata_parts.append(f"Author: {figure_node['author']}")
        if 'license' in figure_node:
            metadata_parts.append(f"License: {figure_node['license']}")
        if 'date' in figure_node:
            metadata_parts.append(f"Date: {figure_node['date']}")
        
        # Add metadata paragraph if we have any metadata
        if metadata_parts:
            metadata_text = ' | '.join(metadata_parts)
            metadata_para = nodes.paragraph(
                text=metadata_text,
                classes=['figure-metadata']
            )
            figure_node.append(metadata_para)


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
    
    for docname in env.found_docs:
        try:
            doctree = env.get_doctree(docname)
            for node in doctree.traverse(nodes.figure):
                if 'license' not in node:
                    # Find the image URI for better error messages
                    image_uri = 'unknown'
                    for image_node in node.traverse(nodes.image):
                        image_uri = image_node.get('uri', 'unknown')
                        break
                    
                    missing_licenses.append((docname, image_uri))
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


def setup(app):
    """
    Setup function for the Sphinx extension.
    
    This function is called by Sphinx to register the extension.
    
    Args:
        app: Sphinx application instance
        
    Returns:
        dict: Extension metadata
    """
    # Override the default figure directive with our custom version
    app.add_directive('figure', CustomFigure, override=True)
    
    # Add custom CSS for metadata styling
    app.add_css_file('custom_figure.css')
    
    # Register event handler to check all figures after build
    app.connect('env-updated', check_all_figures_have_license)
    
    return {
        'version': '0.1.0',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
