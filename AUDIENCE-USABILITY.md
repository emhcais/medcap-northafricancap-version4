# Audience and usability notes

## Stable reference

The design reference is **European Captives v1.2**, the stable map approved in the previous phase. That version remains unchanged. Version 0.3.1 preserves the North African map v0.2 visual shell directly—header, sidebar, summaries, map framing, record list, detail panel, guide, and footer—while making only the approved collection-specific changes.

## Intended audiences

### Primary audiences

- Historians and advanced students working on Mediterranean captivity, conversion, slavery, mobility, and papal Rome.
- Instructors and undergraduate students who need a legible entry point rather than a data-analysis environment.
- Public-history visitors who may arrive with no prior knowledge of the source or its structure.

### Secondary audiences

- Archivists, librarians, and digital-humanities collaborators reviewing data provenance.
- Project maintainers who need a browser-only GitHub Pages deployment without an application server.
- Researchers who prefer downloading the complete collection for their own analysis.

## Stable European map: usability principles to preserve

The European Captives v1.2 map established the following useful baseline:

1. **A stable historical-atlas identity.** The palette, serif headings, compact navigation, and map/sidebar proportion support continuity across the project.
2. **A record list independent of markers.** People without coordinates remain discoverable; absence from the map never means exclusion from the collection.
3. **Plain-language controls.** Search, date range, location view, Reset Filters, a short guide, and one complete CSV download minimize onboarding burden.
4. **Evidence-aware detail panels.** Historical fields appear in a consistent order, and methodological notes sit next to the field they qualify.
5. **Nontechnical publishing.** Visitors need only a browser. Maintainers can publish the prepared files through GitHub Pages.
6. **Conservative change.** Once stable, the map should receive data corrections, accessibility fixes, and documented bug fixes—not aesthetic redesign without a research need.

## Adaptations for this collection

The North African/Ottoman collection retains the stable map’s visual rhythm, large controls, sidebar, guide, Reset Filters behavior, searchable list, record panel, and complete CSV. It changes the interaction model where the source requires it:

- Origins only; no destination markers or connection lines.
- Equal prominence for original and baptismal names.
- Papal Period as a collection-specific filter.
- Four-digit record dates paired with complete source notation; inherited-date status remains explicit in the downloadable CSV.
- Historical place names followed by reviewed modern references in parentheses.
- Explicit distinction among mapped origins, unresolved recorded origins, and records with no origin.

## Usability decisions in this development version

### The list is the primary access path

The map is supplementary. Every record can be found and opened from the list, including records with unresolved places and records without origin data. This supports users who cannot perceive or operate the map and prevents cartographic coverage from controlling historical visibility.

### Both names are searchable

Original and baptismal names are shown side by side on result cards and at the top of the detail view. Neither is treated as a subtitle or alternate identifier.

### Filters combine predictably

Search, location view, date range, Papal Period, and map-point selection are cumulative. Reset Filters restores:

- all records;
- 1600–1699;
- all papal periods;
- no active search;
- no selected map point.

The X on a selected location performs the same complete reset and also clears the displayed location name.

### Uncertainty appears at the point of use

Users should not need to read a separate methodology page to notice a derived value. The record panel labels inferred Clement VIII periods, generalized regional points, and unresolved historical origins. The downloadable CSV separately preserves the original Date cell, inherited Year, effective date, date status, and source citation.

### Accessibility baseline

- Keyboard-visible focus states.
- Native labels, fieldsets, radio buttons, a select dropdown, range outputs, and dialogs.
- Skip link to the records.
- Result count and status text outside the map.
- High-contrast text and controls.
- Responsive single-column layout on narrow screens.
- No information encoded by color alone.
- Reduced-motion preference respected.
- Complete CSV and methodology available when the interactive map is unsuitable.

## Review prompts before stable release

Conduct observation with at least one historian, one student, and one non-specialist. Ask each participant to:

1. Find a person using either name.
2. Isolate a papal period.
3. Explain what an inherited date means.
4. Find a person without a recorded origin.
5. Explain what a regional point does—and does not—claim.
6. Download the complete CSV.
7. Reset the interface without reloading the page.

Record where users hesitate, misinterpret the map, or overlook the evidence flags. Stabilize this companion map only after place-authority review and those tasks can be completed without coaching.
