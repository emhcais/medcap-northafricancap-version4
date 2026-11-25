#!/usr/bin/env python3
"""Acceptance checks for the prepared static application."""
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
payload = json.loads((DATA / "app-data.json").read_text(encoding="utf-8"))
records = payload["records"]

embedded = (DATA / "app-data.js").read_text(encoding="utf-8")
assert embedded.startswith("window.NORTH_AFRICAN_CAPTIVES_DATA = ")
assert embedded.rstrip().endswith(";")
embedded_payload = json.loads(embedded.removeprefix("window.NORTH_AFRICAN_CAPTIVES_DATA = ").rstrip()[0:-1])
assert embedded_payload == payload

assert len(records) == 781
assert Counter(r["dateBasis"] for r in records) == {"explicit": 448, "inherited": 333}
assert Counter(r["papalPeriodBasis"] for r in records) == {"source_section_heading": 773, "inferred_from_date": 8}
assert sum(r["hasOrigin"] for r in records) == 689
assert sum(not r["hasOrigin"] for r in records) == 92
assert sum(r["isMapped"] for r in records) == 475
assert sum(r["hasOrigin"] and not r["isMapped"] for r in records) == 214
assert len(payload["markers"]) == 61
assert len({r["placeOfOrigin"] for r in records if r["hasOrigin"]}) == 269
assert all(r["papalPeriod"] == "Clement VIII" and r["dateYear"] == 1600 for r in records if r["papalPeriodBasis"] == "inferred_from_date")
assert all(r["dateDisplay"] and r["dateIso"] for r in records)
assert all(not (r["dateBasis"] == "inherited" and r["dateSource"]) for r in records)
assert all(r["latitude"] is None and r["longitude"] is None for r in records if not r["hasOrigin"])
assert not any("Rome" in (r["modernPlace"] or "") for r in records)

with (DATA / "north-african-captives-complete.csv").open(encoding="utf-8-sig", newline="") as handle:
    reader = csv.DictReader(handle)
    csv_fields = reader.fieldnames
    csv_rows = list(reader)
assert len(csv_rows) == 781
assert csv_fields is not None
assert "Date" in csv_fields and "Year" in csv_fields and csv_fields.index("Date") < csv_fields.index("Year")
assert all(row["Year"].isdigit() and len(row["Year"]) == 4 for row in csv_rows)
assert sum(not row["Date"] for row in csv_rows) == 333
assert all(row["Source"].startswith("Le baptême des musulmans esclaves à Rome, ") for row in csv_rows)
assert all(row["Effective Date"].startswith(row["Year"]) for row in csv_rows)

html = (ROOT / "index.html").read_text(encoding="utf-8")
js = (ROOT / "app.js").read_text(encoding="utf-8")
for label in ["Original Name", "Baptismal Name", "Place of Origin", "Age", "Date", "Source", "Papal Period"]:
    assert label in js or label in html
for forbidden in ["connection toggle", "Rome marker"]:
    assert forbidden not in html.lower()
assert 'id="papal-period"' in html
assert html.count('type="range"') == 2  # two handles, one overlaid visual timeline
assert 'data/app-data.js' in html
assert "The eight introductory records are assigned to Clement VIII" not in html
assert "The date appears on this source row" not in js
assert "The bold papal heading applies to subsequent people" not in js
assert 'detailRow("Date", String(record.dateYear))' in js
assert "sourceDetailRow(record)" in js
assert "setYearRangeForPeriod(controls.period.value)" in js
assert 'el("clear-selection").addEventListener("click", resetAll)' in js

css_hash = hashlib.sha256((ROOT / "styles.css").read_bytes()).hexdigest()
assert css_hash == "482667e162ef8f7883846c9e49f53886d9dfc36922e2c8d97888e1481cc5a7aa"

print("Acceptance checks passed")
