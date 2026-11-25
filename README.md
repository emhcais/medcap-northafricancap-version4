# Captives from North Africa and the Ottoman World — v0.3.1

A browser-only Leaflet companion map built from **Le Bapteme Des Musulmans Esclaves A Rome-2.xlsx** and prepared for GitHub Pages.

## What changed in v0.3.1

This revision is rebuilt directly from the North African Captives **v0.2 review** package. Its stylesheet is byte-for-byte unchanged from v0.2.

- Preserves the v0.2 header, sidebar, summary boxes, record cards, slide-out panel, help dialog, legend, and two-handle timeline.
- Removes the three requested explanatory notes from the filter and historical-record interface.
- Displays **Date** as a four-digit year.
- Places **Source** immediately under Date as italicized *Le baptême des musulmans esclaves à Rome* followed by the complete applicable source notation.
- Keeps the original Date column in the CSV and adds a numeric Year column, including inherited years for blank source dates.
- Shows only records and origin markers that match the active filters.
- Sets both year handles to the selected Papal Period's earliest and latest represented years.
- Makes the selected-location X reset the search, Papal Period, year range, location mode, selected marker, and displayed location name.

## Collection behavior

- All **781 people** remain searchable.
- Original and baptismal names receive equal prominence.
- Historical records use the seven-field order: Original Name, Baptismal Name, Place of Origin, Age, Date, Source, and Papal Period.
- 475 records have reviewed or generalized map points.
- 214 records have a recorded origin that still awaits place review.
- 92 records have no recorded origin.
- Rome is not mapped as a destination or baptism point, and no route lines are drawn.

## Data rules

See [METHODOLOGY.md](METHODOLOGY.md). In summary:

- 333 blank date cells inherit the preceding explicit date in the numeric Year and Effective Date fields; the original Date cell remains blank and Date Status records the inheritance in the CSV.
- Bold papal headings govern subsequent records until the next heading.
- Eight introductory records dated 1600 are assigned Clement VIII as a marked chronological inference.
- Historical place names appear first; a reviewed modern reference appears in parentheses when needed.
- Unresolved places remain searchable but are deliberately left off the map.

## Preview

The prepared package has no build step. Open `index.html` directly or use GitHub Pages. Leaflet and OpenStreetMap tiles still require an internet connection, but the records are loaded from a local JavaScript data file rather than a browser fetch request.

## Publish on GitHub Pages

See [GITHUB-NEXT-STEPS.md](GITHUB-NEXT-STEPS.md) for a browser-only upload and review checklist.

## Rebuild after a workbook change

The included preparation script uses only Python's standard library. Visitors do not need Python; this command is for a future maintainer:

```bash
python3 scripts/prepare_data.py "Le Bapteme Des Musulmans Esclaves A Rome-2.xlsx" data
python3 scripts/verify_build.py
```

The script regenerates the complete CSV, JSON data, browser-ready JavaScript data, place authority, and build report.

## Release status

This remains a **review release**, not the stable v1.0 companion map. Place-authority review and representative usability testing remain outstanding.
