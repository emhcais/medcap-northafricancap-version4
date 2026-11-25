# Development notes

## Completed in v0.3.1

- Rebuilt directly from the v0.2 review package rather than from v0.3.
- Preserved the full v0.2 stylesheet byte-for-byte.
- Preserved the v0.2 header, sidebar proportions, summary grid, map legend, record list, slide-out panel, guide, and two-handle timeline.
- Made only the requested note, Date, Source, CSV, filter, Papal Period, and location-reset changes.
- Preserved all 781 records and the origin-only map semantics.

## Verification baseline

- 781 person records
- 448 explicit dates and 333 inherited dates
- 773 source-heading papal periods and 8 inferred Clement VIII periods
- 475 mapped records, 214 unresolved recorded origins, and 92 records without an origin
- 269 distinct populated source-origin labels

## Remaining before stable release

1. Review the 214 records whose historical origin labels lack reviewed coordinates.
2. Add gazetteer citations to the place authority.
3. Review modern names and generalized regional points.
4. Complete the usability tasks in `AUDIENCE-USABILITY.md` with representative users.
5. Perform a final visual review on the published GitHub Pages site, including live basemap tiles.
