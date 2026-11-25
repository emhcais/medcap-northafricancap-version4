# Methodology

## Scope

This companion map presents all **781 person records** in *Le Baptême des musulmans esclaves à Rome*. It visualizes documented places of origin only. Rome is not treated as a destination or baptism marker, and the application draws no movement routes.

The source workbook is preserved unchanged. Derived fields make the records filterable while keeping documentary and inferred information distinguishable.

## Inherited-date rule

The workbook contains **448 rows with an explicit date** and **333 blank date cells** among person records.

The approved rule is:

1. Read person records in source-row order.
2. When a person row contains a date, preserve that source string and make it the current effective date.
3. When a person row has a blank date cell, copy the immediately preceding effective date into a separate derived field.
4. Never write the inherited value back into the source-date field.
5. Mark every derived date with `dateBasis = inherited`; explicit dates receive `dateBasis = explicit`.
6. Use the effective date for chronological sorting, the year range control, and papal-period inference where applicable.
7. Display the inherited four-digit year in the historical record while retaining the blank original Date cell in the CSV.
8. If a blank date appeared before any explicit date, stop the build rather than inventing a value. No such case occurs in this workbook.

### Date notation and precision

Dates such as `1600 V.29.` are parsed as year, Roman-numeral month, and day for sorting. The record's **Date** field displays only `1600`; the complete source notation remains visible in the **Source** field and downloadable CSV.

One explicit value is year-level (`1625.0`). It is preserved as written. The application uses January 1 internally only as a sortable convention and marks the record with `datePrecision = year`; January 1 is not presented as an evidenced day.

## Papal-period rule

The workbook uses bold names in the Date column as section headings. The approved rule is:

1. A bold papal heading applies to every subsequent person row until the next bold papal heading.
2. Store the source heading separately in `papalPeriodSource`.
3. Mark these assignments with `papalPeriodBasis = source_section_heading`.
4. Do not treat a heading-derived period as if the pope’s name were repeated on each person row.

The ten documentary headings and resulting counts are:

| Papal Period | Records |
|---|---:|
| Paul V | 74 |
| Grégoire XV | 43 |
| Urbain VIII | 203 |
| Innocent X | 86 |
| Alexandre VII | 88 |
| Clément IX | 19 |
| Clément X | 55 |
| Innocent XI | 132 |
| Alexandre VIII | 11 |
| Innocent XII | 62 |

### Inferred Clement VIII period

Eight people appear under `TABLEAU ANNEXE` before the first papal heading. Their effective dates all fall in **1600**. Because Clement VIII’s pontificate ran from 1592 to 1605, the application assigns **Clement VIII** to these eight records as a chronological inference.

Safeguards:

- `papalPeriodSource` remains `TABLEAU ANNEXE`.
- `papalPeriodBasis` is `inferred_from_date`, not `source_section_heading`.
- The filter labels the period normally, but each affected historical record displays an “Inferred period” flag and explanation.
- The build stops if a Tableau annexe record resolves to a year other than 1600, preventing the rule from silently expanding.
- No other papal period is inferred from dates.

Pontificate reference: Vatican, “Clément VIII,” https://www.vatican.va/content/vatican/fr/holy-father/clemente-viii.html (30 January/9 February 1592–3 March 1605).

## Names and fields

The public historical record always uses this seven-field order:

1. Original Name
2. Baptismal Name
3. Place of Origin
4. Age
5. Date (four-digit year)
6. Source (*Le baptême des musulmans esclaves à Rome*, followed by the complete applicable date notation)
7. Papal Period

Original and baptismal names receive equal visual prominence and are both searchable. Missing values display as “Not recorded.” Age text is preserved verbatim, including uncertainty marks and text-only entries.

## Place authority and modern names

The source contains **689 people with a recorded origin**, **92 without one**, and **269 distinct populated origin labels**.

A separate `data/place-authority.csv` records the historical label, modern reference label, coordinates, location type, confidence, review status, and note. The public display follows these rules:

- Preserve the historical wording first.
- Add a modern reference name in parentheses only when a reviewed identification is available and the wording differs.
- Use reviewed city points where confidence is sufficient.
- Mark region, country, island, or sea points as generalized.
- Leave ambiguous or unresolved places unmapped rather than guessing.
- Keep every person searchable even when no marker can be created.

The current development authority maps **475 records**. A further **214 records have a source origin whose geographic identification still needs review**. The remaining **92 have no source origin**. This is a development snapshot, not a claim that place review is complete.

## Map interpretation

A point represents a reviewed reference for a documented origin label. It does not prove birthplace, route, captivity location, or destination. Multiple people at the same coordinate are aggregated. Broad regional points are intentionally approximate.

## Reproducibility

Run:

```bash
python3 scripts/prepare_data.py "Le Bapteme Des Musulmans Esclaves A Rome-2.xlsx" data
```

The build must reconcile to:

- 781 person records
- 448 explicit dates
- 333 inherited dates
- 8 inferred Clement VIII periods
- 773 periods assigned from source headings
- 689 records with an origin
- 92 records without an origin
- 269 distinct populated origin labels
