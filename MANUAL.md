````{margin}
```{admonition} User types
:class: tip
This section is useful for user type 3-5.
```
````

::::{include} README.md
:end-before: "## Documentation"
::::

## Examples using default settings

### Example 1: Complete Metadata

````md
```{figure} /images/TeachBooks_logo.svg
:name: tb_logo_metadata1
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
:author: Veronica Comin
:date: 2024-11-13
:license: CC-BY
:source: [TeachBooks Logos and Visuals](https://github.com/TeachBooks/logos_and_visualisations)
:copyright: © TeachBooks 2024

The logo of TeachBooks.
```

### Example 2: Minimal Metadata (only a license)

````md
```{figure} /images/TeachBooks_logo.svg
:name: tb_logo_metadata2
:license: CC-BY

The logo of TeachBooks.
```
````

```{figure} /images/TeachBooks_logo.svg
:name: tb_logo_metadata2
:license: CC-BY

The logo of TeachBooks.
```

### Example 3: Without License (generates a warning)

````md
```{figure} /images/TeachBooks_logo.svg
:name: tb_logo_metadata1
:author: Veronica Comin
:date: 2024-11-13
:source: [TeachBooks Logos and Visuals](https://github.com/TeachBooks/logos_and_visualisations)
:copyright: © TeachBooks 2024

The logo of TeachBooks.
```
````

```{figure} /images/TeachBooks_logo.svg
:name: tb_logo_metadata1
:author: Veronica Comin
:date: 2024-11-13
:source: [TeachBooks Logos and Visuals](https://github.com/TeachBooks/logos_and_visualisations)
:copyright: © TeachBooks 2024

The logo of TeachBooks.
```

### Example 4: Invalid License (generates a warning)

````md
```{figure} /images/TeachBooks_logo.svg
:name: tb_logo_metadata1
:author: Veronica Comin
:date: 2024-11-13
:license: Unknown
:source: [TeachBooks Logos and Visuals](https://github.com/TeachBooks/logos_and_visualisations)
:copyright: © TeachBooks 2024

The logo of TeachBooks.
```
````

```{figure} /images/TeachBooks_logo.svg
:name: tb_logo_metadata1
:author: Veronica Comin
:date: 2024-11-13
:license: Unknown
:source: [TeachBooks Logos and Visuals](https://github.com/TeachBooks/logos_and_visualisations)
:copyright: © TeachBooks 2024

The logo of TeachBooks.
```

### Example 5: Placement as an admonition below the caption

````md
```{figure} /images/TeachBooks_logo.svg
:name: tb_logo_metadata1
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
:name: tb_logo_metadata1
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
:name: tb_logo_metadata1
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
:name: tb_logo_metadata1
:author: Veronica Comin
:date: 2024-11-13
:license: CC-BY
:source: [TeachBooks Logos and Visuals](https://github.com/TeachBooks/logos_and_visualisations)
:copyright: © TeachBooks 2024
:placement: margin

The logo of TeachBooks.
```