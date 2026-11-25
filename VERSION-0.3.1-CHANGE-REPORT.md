# Version 0.3.1 file-by-file change report

## Baseline and scope

Version 0.3.1 was copied directly from **North African Captives Map v0.2 review**. The v0.3 redesign was not used as the interface baseline. The package retains the v0.2 page structure and styling and makes only the approved content, data, filtering, and reset changes.

## CSS confirmation

| File | Status | Verification |
|---|---|---|
| `styles.css` | **Unchanged from v0.2** | Byte-for-byte identical; SHA-256 `482667e162ef8f7883846c9e49f53886d9dfc36922e2c8d97888e1481cc5a7aa` |

No CSS rule, selector, declaration, comment, whitespace character, or line ending was changed.

## Modified files

| File | v0.3.1 modification |
|---|---|
| `index.html` | Removed the specified Papal Period explanatory note and its now-unused accessibility reference; updated the existing footer text to point users to the original Date and inherited Year fields in the CSV. The v0.2 header, sidebar, guide, legend, two-handle timeline, record panel, footer structure, and CSV link remain in place. |
| `app.js` | Displays Date as a four-digit year; adds Source immediately below Date with an italicized title and complete applicable date notation; removes the explicit-date and source-section notes; keeps markers and records synchronized with active filters; sets both timeline handles to the selected Papal Period's represented bounds; makes the selected-location X perform the same complete reset as Reset Filters and clears the displayed location name. |
| `scripts/prepare_data.py` | Retains the v0.2 workbook parser, inherited-date rule, papal-period assignments, and place authority; changes the public CSV to preserve the original `Date` column and add numeric `Year`; adds effective-date, source, and transparent derived columns; stamps v0.3.1 metadata. |
| `scripts/verify_build.py` | Adds acceptance checks for Date/Year preservation, all 333 inherited years, complete Source text, removed notes, Papal Period handle logic, complete X reset, and the exact v0.2 CSS hash. |
| `data/north-african-captives-complete.csv` | Regenerated with 781 records; original Date cells remain unchanged and blank where the workbook is blank; Year is numeric and inherited for those 333 blank Date rows; Source contains the title and complete applicable date notation. |
| `data/app-data.json` | Version metadata updated to v0.3.1; the 781 record values, inherited years, coordinates, and place-review statuses remain based on the v0.2 preparation rules. |
| `data/app-data.js` | Browser-ready copy of the same v0.3.1 application data; continues to avoid a runtime JSON fetch. |
| `README.md` | Documents v0.3.1 behavior and the preserved v0.2 design baseline. |
| `CHANGELOG.md` | Adds the v0.3.1 release entry. |
| `DEVELOPMENT-NOTES.md` | Records the direct v0.2 rebuild and limited scope. |
| `GITHUB-NEXT-STEPS.md` | Updates the package name, commit suggestion, and browser review checklist for Papal Period bounds, Date/Source display, CSV columns, and complete X reset. |
| `METHODOLOGY.md` | Updates public Date and Source display rules while retaining the documented inherited-date and papal-period methods. |
| `AUDIENCE-USABILITY.md` | Identifies v0.3.1 as preserving the v0.2 visual shell and documents the selected-location X reset behavior. |
| `SHA256SUMS.txt` | Regenerated after the approved v0.3.1 changes. |
| `VERSION-0.3.1-CHANGE-REPORT.md` | Added this baseline, CSS, modification, unchanged-file, and removal report. |

## Unchanged files

| File | Status |
|---|---|
| `.nojekyll` | Unchanged |
| `styles.css` | Unchanged; exact v0.2 file |
| `COMPARISON-PLAN.md` | Unchanged |
| `PLACE-REVIEW.md` | Unchanged |
| `STABLE-VERSION-REFERENCE.md` | Unchanged |
| `data/build-report.json` | Unchanged because record counts and place coverage are unchanged |
| `data/place-authority.csv` | Unchanged; same reviewed coordinates and unresolved-place statuses as v0.2 |

## Removed file

| File | Reason |
|---|---|
| `VERSION-0.2-CHANGED-FILES.md` | Replaced by this v0.3.1 report to avoid presenting obsolete release instructions. |