# Custom Figure Documentation

Welcome to the Custom Figure extension documentation!

This extension enhances Sphinx's figure directive with metadata support for:
- **Author**: Image creator/author
- **License**: Image license (validated)
- **Date**: Creation date (YYYY-MM-DD format)

## Valid License Types

The following licenses are recognized by the extension:
- Creative Commons: CC0, CC-BY, CC-BY-SA, CC-BY-NC, CC-BY-NC-SA, CC-BY-ND, CC-BY-NC-ND
- Open Source: MIT, Apache-2.0, GPL-3.0, BSD-3-Clause
- Other: Public Domain, Proprietary, All Rights Reserved

## Example Usage

### Example 1: Complete Metadata

```{figure} https://via.placeholder.com/600x400/4A90E2/ffffff?text=Sample+Image+1
:author: John Doe
:license: CC-BY-SA
:date: 2025-01-15
:alt: Sample image with complete metadata
:width: 500px
:align: center

This is a figure with complete metadata including author, license, and date.
```

### Example 2: Minimal Metadata

```{figure} https://via.placeholder.com/600x400/7ED321/ffffff?text=Sample+Image+2
:license: MIT
:alt: Sample image with minimal metadata
:width: 400px

This figure has only a license specified.
```

### Example 3: Without License (Warning)

```{figure} https://via.placeholder.com/600x400/F5A623/ffffff?text=Sample+Image+3
:author: Jane Smith
:alt: Sample image without license
:width: 400px

This figure is missing a license and will generate a warning during build.
```

### Example 4: Invalid License (Warning)

```{figure} https://via.placeholder.com/600x400/BD10E0/ffffff?text=Sample+Image+4
:author: Bob Johnson
:license: InvalidLicense
:date: 2025-01-20
:alt: Sample image with invalid license
:width: 400px

This figure has an invalid license type and will generate a warning.
```

### Example 5: Public Domain Image

```{figure} https://via.placeholder.com/600x400/50E3C2/ffffff?text=Public+Domain
:author: Unknown
:license: Public Domain
:date: 2020-05-10
:alt: Public domain image
:width: 450px
:align: center

This image is in the public domain.
```

## Additional Features

### Caption and Alt Text

All figures should include:
- A descriptive caption (the text below the directive)
- Alt text for accessibility (`:alt:` option)

### Alignment Options

You can align figures using the `:align:` option:
- `left`: Align to the left
- `center`: Center the figure
- `right`: Align to the right

### Width and Scale

Control figure size with:
- `:width:` - Set absolute width (e.g., `500px`, `80%`)
- `:scale:` - Scale percentage (e.g., `50`)

## Validation

During the build process, the extension will:
1. Check if all figures have license information
2. Validate license types against the allowed list
3. Validate date formats (YYYY-MM-DD)
4. Generate warnings for missing or invalid metadata

## Building the Documentation

To build this documentation:

```bash
# Install dependencies
pip install sphinx myst-parser

# Build HTML
sphinx-build -b html . _build/html

# View warnings
# Check the console output for any license-related warnings
```

## Configuration

See `conf.py` for configuration options:
- Enable/disable strict license checking
- Customize valid license list
- Suppress specific warnings

---

*This documentation was generated with the Custom Figure Sphinx extension.*
