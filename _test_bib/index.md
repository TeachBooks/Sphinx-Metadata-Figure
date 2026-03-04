# Full Feature Test

## Test 1: Basic figure with explicit metadata (caption placement)

```{figure} dummy.png
:author: Explicit Author
:license: CC BY
:date: 2024-06-15
:source: https://example.com/source
:placement: caption

Figure with all explicit metadata in caption.
```

## Test 2: Admonition placement

```{figure} dummy.png
:author: Admonition Author
:license: MIT
:date: 2024-01-01
:placement: admonition
:admonition_title: Image Info

Figure with admonition placement.
```

## Test 3: Margin placement

```{figure} dummy.png
:author: Margin Author
:license: CC0
:placement: margin

Figure with margin placement.
```

## Test 4: BibTeX extraction from existing entry

```{figure} dummy.png
:bib: existing_entry
:placement: caption

Figure extracting metadata from existing bib entry.
```

## Test 5: BibTeX generation (single build)

```{figure} dummy.png
:author: Generated Author
:license: CC BY-SA
:date: 2024-07-01
:bib: new_generated_key
:placement: caption

Figure that generates a new bib entry.
```

Citation of generated entry: {cite}`new_generated_key`

## Test 6: Default substitution (no explicit metadata)

```{figure} dummy.png
:placement: caption

Figure with no metadata — should use config defaults (author, date, copyright).
```

## Test 7: Nonumber option (caption without number)

```{figure} dummy.png
:author: Nonumber Author
:license: CC BY
:nonumber:
:placement: caption

This caption should appear without a figure number.
```

## Test 8: Number option (number without caption)

```{figure} dummy.png
:author: Number Author
:license: CC BY
:number:
:placement: caption
```

## Test 9: Figure without image

```{figure}
:author: No Image Author
:license: Public Domain
:placement: caption

A figure with no image but with a caption.
```

## Test 10: Page-level defaults

```{default-metadata-page}
:author: Page Default Author
:license: Apache-2.0
:placement: admonition
```

```{figure} dummy.png

Figure using page-level defaults.
```

## Test 11: Explicit overrides page defaults

```{figure} dummy.png
:author: Override Author
:placement: caption

Figure where explicit author overrides page default.
```

## Test 12: Hide placement

```{figure} dummy.png
:author: Hidden Author
:license: CC BY
:placement: hide

Figure with hidden metadata (validated but not displayed).
```

## Bibliography

```{bibliography}
```
