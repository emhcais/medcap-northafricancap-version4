# Comparison plan: European and North African/Ottoman captive collections

## Principle

Compare the collections at the schema, coverage, and interface level. Do not join people row by row: names are non-unique, exact cross-collection name overlap was not found, and the collections document different historical relationships.

## Stable baseline and companion design

| Dimension | European Captives v1.2 (stable) | North African/Ottoman development map |
|---|---|---|
| Collection size | 3,137 records | 781 records |
| Spatial evidence | Origin, captivity place, documented connection | Documented origin only |
| Core identity | One principal captive name | Original and baptismal names equally prominent |
| Collection fields | Origin, captivity, convert, date, ship, source, notes, ID | Original name, baptismal name, origin, age, date, Papal Period |
| Chronology | Year-oriented date filtering with normalization notes | Roman-month parsing, 333 inherited dates, Papal Period filter |
| Missing geography | Dedicated No Location Data access | Dedicated No Location Data access plus unresolved-origin notes |
| Map movement | Connections may be shown | No movement, destination, Rome, or baptism marker |
| Release state | Stable; preserve | Development; place review and usability study outstanding |

## What remains consistent

- Historical-atlas brand family.
- Serif display type paired with a readable sans serif UI.
- Sidebar plus map arrangement.
- Search, date controls, Reset Filters, record count, guide, and one complete CSV.
- Record access independent of map coverage.
- Source wording preserved in public records.
- Method notes placed next to affected fields.
- OpenStreetMap/Leaflet browser-only deployment.

## What must remain different

- Spatial semantics and legend.
- Record fields.
- Papal Period filter.
- Two-name presentation.
- Inherited-date and inferred-period indicators.
- Historical/modern place-name presentation.
- No connection toggle or route lines.

## Comparable measures for future research

Use collection-level measures that do not imply person-level equivalence:

- total records;
- explicit versus derived date coverage;
- origin coverage;
- proportion mapped after review;
- distinct source place labels;
- records by 25-year band;
- most frequent reviewed origins;
- percentage of records with each collection-specific field populated.

Any combined portal should append both datasets to a canonical schema containing `collection`, `record_id`, `name_primary`, `name_secondary`, `date_display`, `date_basis`, `origin_source`, `origin_modern`, and collection-specific metadata. Preserve each map as an independent interpretive view.
