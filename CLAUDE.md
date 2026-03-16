# Sphinx-Metadata-Figure — Claude Session Notes

## Project Overview
Sphinx extension (`sphinx_metadata_figure`) that adds metadata (author, license, date, source, copyright) to figure directives and optionally generates BibTeX entries for them.

Main source: `src/sphinx_metadata_figure/__init__.py` (~1600 lines)

## Key Functions
- `_generate_bib_entry()` — builds a `@misc{...}` BibTeX string from figure metadata
- `_write_bib_entries_atomic()` (MEDIUM branch) / `_write_bib_entry()` (main) — writes to `.bib` file
- `_parse_bib_entry()` — parses a BibTeX entry from file content
- `_resolve_bib_output_path()` — resolves output path relative to `app.srcdir`
- `_scan_source_for_bib_figures()` — scans `.md`, `.rst`, `.ipynb` for figures with `:bib:` option
- `pre_generate_bib_entries()` — Sphinx `config-inited` hook; orchestrates BibTeX pre-generation
- `_escape_bibtex_field()` — (CRITICAL branch only) escapes unbalanced braces in field values

## Session Work (2026-03-16)
Created 4 separate fix branches from `main`, each targeting a specific severity tier.
**All branches are pushed; PRs need to be created manually** (no `gh` CLI, no GitHub token).

### PR 1 — CRITICAL (`claude/fix-critical-security-tinyc`)
- `_resolve_bib_output_path`: validate resolved path stays within `app.srcdir` (path traversal fix)
- Added `_escape_bibtex_field()` helper; applied to all metadata fields in `_generate_bib_entry`
- PR URL: https://github.com/TeachBooks/Sphinx-Metadata-Figure/pull/new/claude/fix-critical-security-tinyc

### PR 2 — HIGH (`claude/fix-high-issues-tinyc`)
- Replaced regex-based BibTeX field extraction with a character-level brace scanner (handles arbitrary nesting)
- Guard `bibtex_bibfiles.append()` against immutable tuple type
- PR URL: https://github.com/TeachBooks/Sphinx-Metadata-Figure/pull/new/claude/fix-high-issues-tinyc

### PR 3 — MEDIUM (`claude/fix-medium-issues-tinyc`)
- Replaced delete+write-per-entry with `_write_bib_entries_atomic()` using `tempfile` + `os.replace()`
- `json.JSONDecodeError` now logged at `warning` (was `debug`)
- Simplified metadata dict construction with dict comprehension
- PR URL: https://github.com/TeachBooks/Sphinx-Metadata-Figure/pull/new/claude/fix-medium-issues-tinyc

### PR 4 — LOW (`claude/fix-low-issues-tinyc`)
- Default `output_file` changed from hardcoded `_build/_temp/` to `app.outdir/_temp/`
- Replaced O(n²) `bib_content +=` string growth with a `generated_keys` set
- PR URL: https://github.com/TeachBooks/Sphinx-Metadata-Figure/pull/new/claude/fix-low-issues-tinyc

## Development Branch Convention
- Branch names must start with `claude/` and end with session suffix (e.g. `tinyc`)
- `gh` CLI is NOT available — use Gitea/GitHub API or manual PR creation
- The git remote proxy at `127.0.0.1:37302` only supports git operations, not REST API calls
- GitHub API is accessible directly (`api.github.com`) but no token is configured
