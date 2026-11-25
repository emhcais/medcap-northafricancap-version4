# Historical-place review workflow

The development map intentionally separates documentary labels from geographic interpretation.

## Authority file

Review `data/place-authority.csv` in descending `record_count` order. Each row includes:

- original source label;
- normalized search label;
- record count;
- modern reference label;
- coordinates;
- location type;
- confidence;
- review status;
- reviewer note.

## Review standard

1. Preserve the source label exactly.
2. Consult historical gazetteers and scholarship, not only a modern geocoder.
3. Record the source for each new identification in the reviewer note or a future source column.
4. Distinguish city, island, region, country, sea, and ambiguous labels.
5. Use regional points only when the source itself is regional; mark them generalized.
6. Do not resolve ambiguous names by convenience. Leave coordinates blank.
7. Add the modern name only when it materially helps orientation.
8. Never create a Rome destination or infer a route.

## Release gate

Before declaring the companion map stable:

- review every high-frequency unresolved label;
- add authority-source citations;
- sample every reviewed label against its associated records;
- confirm that modern names do not overwrite source wording;
- repeat the acceptance counts in `METHODOLOGY.md`;
- complete the usability tasks in `AUDIENCE-USABILITY.md`.
