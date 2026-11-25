# Changelog

## v0.3.1 — 2026-11-25

- Rebuilt directly from v0.2 and preserved `styles.css` without any byte change.
- Removed the three specified explanatory notes.
- Changed historical-record Date display to a four-digit year.
- Added Source directly beneath Date with the italicized title and complete original date notation.
- Preserved the original CSV Date column and added numeric Year values, including inherited years.
- Kept record and origin-marker results synchronized with active filters.
- Made Papal Period selection move both timeline handles to the represented year bounds.
- Made the selected-location X perform a complete reset, including clearing the displayed location name.

## v0.2-review — 2026-11-25

- Rebased the interface on the stable European Captives v1.2 historical-atlas template.
- Added the complete site header, summary grid, slide-out record panel, guide dialog, and footer in the stable-map style.
- Consolidated the visibly separate date controls into one overlaid range timeline.
- Replaced Papal Period checkboxes with a dropdown.
- Added `data/app-data.js` to remove the startup fetch dependency and improve direct-file/GitHub Pages loading reliability.
- Kept one public download: the complete CSV.
- Added GitHub upload, publishing, troubleshooting, and acceptance instructions.
- Preserved the 781-record data model, inherited-date rule, inferred Clement VIII rule, and reviewed-place coverage.

## v0.1-development

- Initial North African/Ottoman companion-map development package.
- Prepared all 781 records and the historical-place authority.
- Implemented search, date, papal-period, and location-status filtering.
