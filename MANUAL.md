````{margin}
```{admonition} User types
:class: tip
This section is useful for user type 3-5.
```
````

````{margin}

```{note}

{bdg-primary}`Sphinx Extension`
{bdg-link-light}`Included in TeachBooks Template <../../external/template/README.html>`
{bdg-link-light}`Included in TeachBooks Favourites <../../features/favourites.html>`

```

```{tip}
This section is useful for user type 3-5.
```

```{seealso}

[{octicon}`mark-github` Repository](https://github.com/TeachBooks/Sphinx-Metadata-Figure)

[{octicon}`book` Copyright and Licenses checklist](../../workflows/collaboration.md)

```

````


::::{include} README.md
:end-before: "## Documentation"
::::

## Examples using default settings

These examples assume that the config only has the default options except for the `placement`, `summaries`, and `individual` options which are set as follows:

```yaml
sphinx:
  config:
    metadata_figure_settings:
      style: 
        placement: caption
      license:
        summaries: true
        individual: true
```

### Example 1: Complete Metadata

````md
```{figure} /images/TeachBooks_logo.svg
:name: tb_logo_metadata1
:width: 50%
:author: Veronica Comin
:date: 2024-11-13
:license: CC-BY
:source: [TeachBooks Logos and Visuals](https://github.com/TeachBooks/logos_and_visualisations)
:copyright: © TeachBooks 2024

The logo of TeachBooks.
```
````

```{figure} /images/TeachBooks_logo.svg
:name: tb_logo_metadata1
:width: 50%
:author: Veronica Comin
:date: 2024-11-13
:license: CC-BY
:source: [TeachBooks Logos and Visuals](https://github.com/TeachBooks/logos_and_visualisations)
:copyright: © TeachBooks 2024
:placement: caption

The logo of TeachBooks.
```

### Example 2: Minimal Metadata (only a license)

````md
```{figure} /images/TeachBooks_logo.svg
:name: tb_logo_metadata2
:width: 50%
:license: CC-BY

The logo of TeachBooks.
```
````

```{figure} /images/TeachBooks_logo.svg
:name: tb_logo_metadata2
:width: 50%
:license: CC-BY
:placement: caption

The logo of TeachBooks.
```

### Example 3: Without License (generates a warning)

````md
```{figure} /images/TeachBooks_logo.svg
:name: tb_logo_metadata3
:width: 50%
:author: Veronica Comin
:date: 2024-11-13
:source: [TeachBooks Logos and Visuals](https://github.com/TeachBooks/logos_and_visualisations)
:copyright: © TeachBooks 2024

The logo of TeachBooks.
```
````

```{figure} /images/TeachBooks_logo.svg
:name: tb_logo_metadata3
:width: 50%
:author: Veronica Comin
:date: 2024-11-13
:source: [TeachBooks Logos and Visuals](https://github.com/TeachBooks/logos_and_visualisations)
:copyright: © TeachBooks 2024
:placement: caption

The logo of TeachBooks.
```

### Example 4: Invalid License (generates a warning)

````md
```{figure} /images/TeachBooks_logo.svg
:name: tb_logo_metadata4
:width: 50%
:author: Veronica Comin
:date: 2024-11-13
:license: Unknown
:source: [TeachBooks Logos and Visuals](https://github.com/TeachBooks/logos_and_visualisations)
:copyright: © TeachBooks 2024

The logo of TeachBooks.
```
````

```{figure} /images/TeachBooks_logo.svg
:name: tb_logo_metadata4
:width: 50%
:author: Veronica Comin
:date: 2024-11-13
:license: Unknown
:source: [TeachBooks Logos and Visuals](https://github.com/TeachBooks/logos_and_visualisations)
:copyright: © TeachBooks 2024
:placement: caption

The logo of TeachBooks.
```

### Example 5: Placement as an admonition below the caption

````md
```{figure} /images/TeachBooks_logo.svg
:name: tb_logo_metadata5
:width: 50%
:author: Veronica Comin
:date: 2024-11-13
:license: CC-BY
:source: [TeachBooks Logos and Visuals](https://github.com/TeachBooks/logos_and_visualisations)
:copyright: © TeachBooks 2024
:placement: admonition

The logo of TeachBooks.
```
````

```{figure} /images/TeachBooks_logo.svg
:name: tb_logo_metadata5
:width: 50%
:author: Veronica Comin
:date: 2024-11-13
:license: CC-BY
:source: [TeachBooks Logos and Visuals](https://github.com/TeachBooks/logos_and_visualisations)
:copyright: © TeachBooks 2024
:placement: admonition

The logo of TeachBooks.
```

### Example 6: Placement as an admonition in the margin

````md
```{figure} /images/TeachBooks_logo.svg
:name: tb_logo_metadata6
:width: 50%
:author: Veronica Comin
:date: 2024-11-13
:license: CC-BY
:source: [TeachBooks Logos and Visuals](https://github.com/TeachBooks/logos_and_visualisations)
:copyright: © TeachBooks 2024
:placement: margin

The logo of TeachBooks.
```
````

```{figure} /images/TeachBooks_logo.svg
:name: tb_logo_metadata6
:width: 50%
:author: Veronica Comin
:date: 2024-11-13
:license: CC-BY
:source: [TeachBooks Logos and Visuals](https://github.com/TeachBooks/logos_and_visualisations)
:copyright: © TeachBooks 2024
:placement: margin

The logo of TeachBooks.
```


### Example 7: Hidden Metadata

````md
```{figure} /images/TeachBooks_logo.svg
:name: tb_logo_metadata7
:width: 50%
:author: Veronica Comin
:date: 2024-11-13
:license: CC-BY
:source: [TeachBooks Logos and Visuals](https://github.com/TeachBooks/logos_and_visualisations)
:copyright: © TeachBooks 2024
:placement: hide

The logo of TeachBooks.
```
````

```{figure} /images/TeachBooks_logo.svg
:name: tb_logo_metadata6
:width: 50%
:author: Veronica Comin
:date: 2024-11-13
:license: CC-BY
:source: [TeachBooks Logos and Visuals](https://github.com/TeachBooks/logos_and_visualisations)
:copyright: © TeachBooks 2024
:placement: hide

The logo of TeachBooks.
```

::::{include} README.md
:start-after: "<!-- Start contribute -->"
::::
