# Figure Metadata Extension

A Sphinx extension that provides an interface to add metadata to figures and display the metadata.

This extension enhances Sphinx's figure directive and the [MyST-NB sphinx extension's `glue:figure` directive](https://myst-nb.readthedocs.io/en/latest/render/glue.html#the-glue-figure-directive) with metadata support for:
- **Author**: Image creator/author
- **License**: Image license (validated):
  - a full list of the valid license types is available in the [TeachBooks manual](https://teachbooks.io/manual/_git/github.com_TeachBooks_Sphinx-Metadata-Figure/main/MANUAL.html#recognized-licenses).
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
        placement: hide
        show: author,license,date,copyright,source
        admonition_title: Attribution
        admonition_class: attribution
      license:
        link_license: true
        strict_check: false
        summaries: false
        individual: false
        substitute_missing: false
        default_license: CC BY
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
      bib:
        extract_metadata: true
```

Each of the level 1 keys in `metadata_figure_settings` must be a dictionary of key-value pairs. Each level 1 ley will be discussed next, including the options.

### Style

The `style` key contains options for how the metadata is displayed.
- `placement`: Where to place the metadata. Options are
  - `caption`: as text on a new line in the figure caption. If no figure caption is provided by the user, the metadata will still be added as a caption without introducing figure numbering.
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
- a full list of the valid license types is available in the [TeachBooks manual](https://teachbooks.io/manual/_git/github.com_TeachBooks_Sphinx-Metadata-Figure/main/MANUAL.html#recognized-licenses).

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

### Bib

The `bib` key contains options for BibTeX entry support. This allows you to extract figure metadata from existing BibTeX entries.

Configuration options:
- `extract_metadata`: If `true`, metadata will be extracted from existing BibTeX entries when the `:bib:` option references a valid key. Default: `true`.

## Usage

The figure directive and the [MyST-NB sphinx extension's `glue:figure` directive](https://myst-nb.readthedocs.io/en/latest/render/glue.html#the-glue-figure-directive) are extended with the following options to add metadata:

- `author`:
  - Optionally specify the author/creator of the image.
- `license`:
  - Specify the license type of the image. Must be one of the valid license types.
- `date`:
  - Optionally specify the creation date of the image.
  - This value can be:
    - a date in `YYYY-MM-DD` format
    - `today`, which will result in using the date at which the build is performed.
- `copyright`:
  - Optionally specify a text with copyright information for the image.
- `source`:
  - Optionally specify the source of the image.
  - This value can be:
    - a URL (starting with "http" or "https")
    - a textual source description
    - a MarkDown link
    - `document`, which will result in inserting a MarkDown link of the form `[Source code](url_to_parent_document_that_contains_the_figure_directive)`.
- `placement`:
  - Optionally override the global `placement` setting for this figure only.
  - Options are `caption`, `admonition`, `margin` or `hide`.
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
- `bib`:
  - Optionally specify a BibTeX key for this figure.
  - When specified with an existing key in your `.bib` files, metadata (author, date, source, license) will be extracted from the BibTeX entry using the following mapping:
    | Metadata Field | Primary BibTeX Source | Fallback BibTeX source | Notes |
    |---|---|---|---|
    | `author` | `author` field | — | Used as-is |
    | `date` | `date` field | `year` field | If only `year` exists, converted to `YYYY-01-01` format |
    | `source` | `url` field | `howpublished` field | If `howpublished` contains `\url{...}`, extracts the URL; otherwise uses full value if `url` not present |
    | `license` | `note` field | — | Only extracted if formatted as `license: ...` (case-insensitive); the text after the prefix is used |
    | `copyright` | `copyright` field | — | Used as-is |
  - Fields that cannot be extracted are simply omitted from metadata (no defaults applied at extraction time)
  - Explicit metadata options (`:author:`, `:license:`, etc.) take precedence over extracted bib metadata.
  - The BibTeX entry is also automatically added to the document bibliography using a `cite:empty` role (when the BibTeX key exists).

## Setting Page-Level Defaults

You can set default metadata values for all figures on a specific page using the `default-metadata-page` directive. This provides a middle layer between global configuration and per-figure settings.

### Syntax

```rst
.. default-metadata-page::
   :author: John Doe
   :license: CC-BY
   :placement: admonition
```

Or in MyST markdown:

```markdown
```{default-metadata-page}
:author: John Doe
:license: CC-BY
:placement: admonition
```
```

### Features

- **Scope**: Applies to all figures in the current document only
- **Priority**: Page defaults override global config and BibTeX metadata, but are overridden by explicit figure options
- **All options supported**: You can set any metadata field or display option at page level

### Priority Order

When determining metadata values, the extension follows this priority chain (highest to lowest):

1. **Explicit figure option** (`:author:` on the figure directive)
2. **Page-level default** (from `default-metadata-page`)
3. **BibTeX metadata** (when `:bib:` references an existing entry)
4. **Global configuration** (from `_config.yml`)

For detailed examples and usage, see the [Page-Level Defaults section in the manual](https://teachbooks.io/manual/_git/github.com_TeachBooks_Sphinx-Metadata-Figure/main/MANUAL.html#page-level-defaults).

## Documentation

Further documentation for this extension is available in the [TeachBooks manual](https://teachbooks.io/manual/_git/github.com_TeachBooks_Sphinx-Metadata-Figure/main/MANUAL.html).

<!-- Start contribute -->
## Contribute

This tool's repository is stored on [GitHub](https://github.com/TeachBooks/Sphinx-Metadata-Figure). If you'd like to contribute, you can create a fork and open a pull request on the [GitHub repository](https://github.com/TeachBooks/Sphinx-Metadata-Figure).
