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
        individual: false
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
  - `caption`: as text on a new line in the figure caption.
  - `admonition`: in an admonition box below the figure caption.
  - `margin`: in an admonition in the margin next to the figure.
  - `hide`: The metadata is not added to the output, but is verified.
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

The `license` key contains options for how to handle license metadata.
- `link_license`: If `true`, the license name will be a hyperlink to the license text (if known).
- `strict_check`: If `true`, an error will be generated for the first figure without license information or with an invalid license type.
- `summaries`: If `true`, a short summary of all figures without a license or with an invalid license type will be shown during the build.
- `individual`: If `true`, each figure with missing or invalid license information will generate a separate warning. Value is irrelevant if `strict_check` is `true`.
- `substitute_missing`: If `true`, figures without license information will use the `default_license` value. No warning will be generated if this is set to `true`.
- `default_license`: The default license to use if `substitute_missing` is `true`.

All licenses are validated against the following predefined list of valid license types:
- Creative Commons: CC0, CC-BY, CC-BY-SA, CC-BY-NC, CC-BY-NC-SA, CC-BY-ND, CC-BY-NC-ND
- Open Source: MIT, Apache-2.0, GPL-3.0, BSD-3-Clause
- Other: Public Domain, Proprietary, All Rights Reserved

### Author
The `author` key contains options for how to handle author metadata.
- `substitute_missing`: If `true`, figures without author information will use a value based on the `default_author` option.
- `default_author`: The default author to use if `substitute_missing` is `true`. Options are:
  - `config`: Use the `author` value from the Sphinx configuration.
  - Any other string value will be used as the default author.

### Date
The `date` key contains options for how to handle date metadata.
- `substitute_missing`: If `true`, figures without date information will use a value based on the `default_date` option.
- `default_date`: The default date to use if `substitute_missing` is `true`. Options are:
  - `today`: Use date at which the build is performed.
  - Any other string value in `YYYY-MM-DD` format will be used as the default date.

### Copyright

The `copyright` key contains options for how to handle copyright metadata.
- `substitute_missing`: If `true`, figures without copyright information will use a value based on the `default_copyright` option.
- `default_copyright`: The default copyright to use if `substitute_missing` is `true`. Options are:
  - `authoryear`: Use a string in the format `Year Author`. If the author is missing, only the year will be used. If the date is missing, only the author will be used. If both are missing, no copyright will be shown.
  - `config`: Use the `copyright` value from the Sphinx configuration.
  - `authoryear-config`: Use a string in the format `Year Author` as described above, but if both the author and date are missing, use the Sphinx configuration value instead.
  - `config-authoryear`: Use the Sphinx configuration value, but if that is missing, use the `Year Author` format as described above.
  - Any other string value will be used as the default copyright.

### Source

The `source` key contains options for how to handle source metadata.
- `warn_missing`: If `true`, a warning will be generated for each figure without source information.

## Usage

The figure directive is extended with the following options to add metadata:

- `author`:
  - Optionally specify the author/creator of the image.
- `license`:
  - Specify the license type of the image. Must be one of the valid license types.
- `date`:
  - Optionally specify the creation date of the image in `YYYY-MM-DD` format.
- `copyright`:
  - Optionally specify a text with copyright information for the image.
- `source`:
  - Optionally specify the source of the image.
  - This value can be:
    - a URL (starting with "http" or "https")
    - a textual source description
    - a MarkDown link
- `placement`:
  - Optionally override the global `placement` setting for this figure only.
  - Options are `caption`, `admonition`, or `margin`.
- `show`:
  - Optionally override the global `show` setting for this figure only.
  - Comma-separated list of which metadata fields to show.
  - Options are any combination of `author`, `license`, `date`, `copyright` and `source`.
- `admonition_title`:
  - Optionally override the global `admonition_title` setting for this figure only.
  - Only relevant if `placement` is `admonition` or `margin`.
- `admonition_class`:
  - Optionally override the global `admonition_class` setting for this figure only.
  - Only relevant if `placement` is `admonition` or `margin`.

## Documentation

Further documentation for this extension is available in the [TeachBooks manual](https://teachbooks.io/manual).

## Contribute

This tool's repository is stored on [GitHub](https://github.com/TeachBooks/Sphinx-Metadata-Figure). If you'd like to contribute, you can create a fork and open a pull request on the [GitHub repository](https://github.com/TeachBooks/Sphinx-Metadata-Figure).