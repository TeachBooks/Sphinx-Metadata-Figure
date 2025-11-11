# Custom Figure Sphinx Extension

A Sphinx extension that enhances the standard `figure` directive with metadata support (author, license, date) and automatic license validation for MyST Markdown documents.

## Features

- ✅ Add **author**, **license**, and **date** metadata to figures
- ✅ Automatic **license validation** against a predefined list
- ✅ **Build-time warnings** for missing or invalid licenses
- ✅ Compatible with both **reStructuredText** and **MyST Markdown**
- ✅ Optional **metadata display** below figures
- ✅ Customizable CSS styling

## Installation

### Prerequisites

```bash
pip install sphinx myst-parser
```

### Project Structure

```
sphinx_custom_figure_project/
├── _ext/
│   └── custom_figure.py      # Custom figure directive extension
├── _static/
│   └── custom_figure.css     # Styling for figure metadata
├── conf.py                    # Sphinx configuration
├── index.md                   # Main documentation file
└── README.md                  # This file
```

## Quick Start

1. **Configure Sphinx** (`conf.py`):
   ```python
   import sys
   from pathlib import Path
   
   sys.path.insert(0, str(Path('_ext').resolve()))
   
   extensions = [
       'myst_parser',
       'custom_figure',
   ]
   ```

2. **Use in MyST Markdown**:
   ````markdown
   ```{figure} path/to/image.png
   :author: John Doe
   :license: CC-BY-SA
   :date: 2025-01-15
   :width: 500px
   
   Your figure caption here.
   ```
   ````

3. **Build documentation**:
   ```bash
   sphinx-build -b html . _build/html
   ```

## Usage

### Basic Example

````markdown
```{figure} image.png
:author: Jane Smith
:license: MIT
:date: 2025-01-20
:alt: A sample image
:width: 400px

This is a sample figure with metadata.
```
````

### Supported Licenses

The extension validates against these licenses:
- **Creative Commons**: CC0, CC-BY, CC-BY-SA, CC-BY-NC, CC-BY-NC-SA, CC-BY-ND, CC-BY-NC-ND
- **Open Source**: MIT, Apache-2.0, GPL-3.0, BSD-3-Clause
- **Other**: Public Domain, Proprietary, All Rights Reserved

### Directive Options

| Option | Required | Description | Example |
|--------|----------|-------------|---------|
| `author` | No | Image creator/author | `John Doe` |
| `license` | Recommended | Image license | `CC-BY-SA` |
| `date` | No | Creation date (YYYY-MM-DD) | `2025-01-15` |

All standard Sphinx figure options are also supported:
- `:width:` - Set width
- `:height:` - Set height
- `:scale:` - Scale percentage
- `:alt:` - Alternative text
- `:align:` - Alignment (left, center, right)
- `:name:` - Reference name

## Validation

### Build-Time Checks

During the build process, the extension:
1. ✅ Warns if a figure is missing license information
2. ✅ Validates license types against the allowed list
3. ✅ Checks date format (YYYY-MM-DD)
4. ✅ Generates detailed warning messages with file location

### Example Warnings

```
WARNING: Figure "image.png" at docs/page.md:42 is missing license information.
WARNING: Figure "photo.jpg" at docs/page.md:67 has invalid license "CUSTOM-LICENSE".
WARNING: Figure "diagram.svg" at docs/page.md:89 has invalid date format "2025/01/15".
```

## Customization

### Modify Valid Licenses

Edit `_ext/custom_figure.py`:

```python
VALID_LICENSES = [
    'CC0',
    'CC-BY',
    'Your-Custom-License',
    # Add your licenses here
]
```

### Disable Metadata Display

In `custom_figure.py`, comment out the metadata display call:

```python
# self._add_metadata_display(figure_node)
```

### Custom CSS Styling

Edit `_static/custom_figure.css` to customize the appearance of metadata.

### Strict Mode (Fail on Missing License)

To make the build fail when licenses are missing, modify the `check_all_figures_have_license` function in `custom_figure.py` to raise an exception instead of logging a warning.

## Testing

Build the sample documentation to see the extension in action:

```bash
# Navigate to project directory
cd sphinx_custom_figure_project

# Build HTML documentation
sphinx-build -b html . _build/html

# Open in browser
# Linux/Mac:
open _build/html/index.html
# Windows:
start _build/html/index.html
```

## Configuration Options

In `conf.py`, you can configure:

```python
# Suppress license warnings (not recommended)
suppress_warnings = ['custom_figure.missing_license']

# Enable strict license checking (custom implementation required)
STRICT_LICENSE_CHECK = True
```

## Extending the Extension

### Add New Metadata Fields

1. Add to `option_spec` in `CustomFigure` class
2. Add validation logic in the `run()` method
3. Update `_add_metadata_display()` to show the new field

Example:
```python
option_spec.update({
    'copyright': directives.unchanged,
    'source': directives.unchanged,
})
```

### Custom Validation Rules

Add custom validation in the `run()` method:

```python
# Validate author format
author = self.options.get('author', None)
if author and '@' in author:
    logger.warning('Author should be a name, not an email')
```

## Troubleshooting

### Extension Not Found

Make sure `_ext` directory is in Python path:
```python
sys.path.insert(0, str(Path('_ext').resolve()))
```

### CSS Not Loading

Verify `html_static_path` in `conf.py`:
```python
html_static_path = ['_static']
```

### Warnings Not Appearing

Check Sphinx warning level:
```bash
sphinx-build -W -b html . _build/html  # Treat warnings as errors
sphinx-build -v -b html . _build/html   # Verbose output
```

## Contributing

To contribute to this extension:
1. Add new features or fix bugs in `_ext/custom_figure.py`
2. Update documentation in `index.md`
3. Test with various figure configurations
4. Update this README

## License

This extension is released under the MIT License.

## Resources

- [Sphinx Documentation](https://www.sphinx-doc.org/)
- [MyST Parser Documentation](https://myst-parser.readthedocs.io/)
- [Docutils Directives](https://docutils.sourceforge.io/docs/ref/rst/directives.html)

## Support

For issues or questions:
- Check the Sphinx documentation for general Sphinx issues
- Review MyST Parser docs for MyST-specific questions
- Examine the code in `_ext/custom_figure.py` for extension behavior

---

**Created**: October 2025  
**Version**: 0.1.0  
**Author**: Custom Figure Extension Team
