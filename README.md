# Figure Metadata Extension

A Sphinx extension that provides an interface to add metadata to figures and display the metadata.

This extension enhances Sphinx's figure directive with metadata support for:
- **Author**: Image creator/author
- **License**: Image license (validated)
- **Date**: Creation date (YYYY-MM-DD format)
- **Copyright**: Copyright holder
- **Source**: Image source

## Installation
To install the Sphinx-Metadata-Figure extension, follow these steps:

**Step 1: Install the Package**

Install the `Sphinx-Metadata-Figure` package using `pip`:
```
pip install sphinx-metadata-figure
```

**Step 2: Add to `requirements.txt`**

Make sure that the package is included in your project's `requirements.txt` to track the dependency:
```
sphinx-metadata-figure
```

**Step 3: Enable in `_config.yml`**

In your `_config.yml` file, add the extension to the list of Sphinx extra extensions:
```
sphinx: 
    extra_extensions:
        - sphinx_metadata_figure
```

## Configuration

This extension can be configured via the `_config.yml` file in your JupyterBook project (or similarly in `conf.py` for standard Sphinx projects).

The _default_ configuration options are as follows:

```yaml
sphinx:
  config:
    metadata_figure_settings:
      style: 
        placement: caption
        show: author,license,date,copyright,source
        admonition_title: Attribution
        admonition_class: attribution
      license:
        link_license: true
        strict_check: false
        summaries: true
        individual: true
        substitute_missing: false
        default_license: CC-BY
      author:
        substitute_missing: false
        default_author: config
      date:
        substitute_missing: false
        default_date: today
      copyright:
        substitute_missing: false
        default_copyright: authoryear
      source:
        warn_missing: false
```

Each of the level 1 keys in `metadata_figure_settings` must be a dictionary of key-value pairs. Each level 1 ley will be discussed next, including the options.

### Style

The `style` key contains options for how the metadata is displayed.
- `placement`: Where to place the metadata. Options are
 - `caption`: as text below the figure caption.
 - `admonition`: in an admonition box below the figure caption.
 - `margin`: in an admonition in the margin next to the figure.
- `show`: A comma-separated list of which metadata fields to show. Options that can be included are
  - `author`
  - `license`
  - `date`
  - `copyright`
  - `source`
- `admonition_title`: (English) title of the admonition box (if `placement` is `admonition` or `margin`). Will be translated if translations are available.
- `admonition_class`: CSS class to apply to the admonition box.

The last two options are only relevant if `placement` is set to `admonition` or `margin`.

### License





































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
:source: https://www.google.com/search?q=COPYRIGHT&rlz=1C1GCHA_enNL1151NL1151&oq=COPYRIGHT&gs_lcrp=EgZjaHJvbWUyBggAEEUYOdIBBzYyMmowajeoAgCwAgA&sourceid=chrome&ie=UTF-8

This is a figure with complete metadata including author, license, and date.
```

### Example 2: Minimal Metadata

```{figure} https://via.placeholder.com/600x400/7ED321/ffffff?text=Sample+Image+2
:license: MIT
:alt: Sample image with minimal metadata
:width: 400px
:source: [pretty source](https://www.google.com/search?q=COPYRIGHT&rlz=1C1GCHA_enNL1151NL1151&oq=COPYRIGHT&gs_lcrp=EgZjaHJvbWUyBggAEEUYOdIBBzYyMmowajeoAgCwAgA&sourceid=chrome&ie=UTF-8)

This figure has only a license specified.
```

### Example 3: Without License (Warning)

```{figure} https://via.placeholder.com/600x400/F5A623/ffffff?text=Sample+Image+3
:author: Jane Smith
:alt: Sample image without license
:width: 400px
:source: Ergens vandaan

This figure is missing a license and will generate a warning during build.
```

### Example 4: Invalid License (Warning)

```{figure} https://via.placeholder.com/600x400/BD10E0/ffffff?text=Sample+Image+4
:author: Bob Johnson
:license: invalid-license
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

## Contents

```{toctree}
:maxdepth: 1

reference/contact_information
```