#!/usr/bin/env python3
"""Build the North African/Ottoman captives map data from the source XLSX.

This script deliberately uses only Python's standard library. It reads the XLSX
as an OOXML ZIP package, preserves source wording, applies the approved inherited-
date rule, and assigns papal periods from bold source headings. The eight Tableau
annexe records dated in 1600 are assigned Clement VIII as an explicitly marked
chronological inference.
"""
from __future__ import annotations

import csv
import json
import re
import sys
import unicodedata
import xml.etree.ElementTree as ET
from collections import Counter
from datetime import date
from pathlib import Path
from zipfile import ZipFile

MAIN_NS = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
NS = {"m": MAIN_NS}
SOURCE_TITLE = "Le baptême des musulmans esclaves à Rome"

HEADINGS = {
    "TABLEAU ANNEXE",
    "PAUL V",
    "GREGOIRE XV",
    "URBAIN VIII",
    "INNOCENT X",
    "ALEXANDRE VII",
    "CLEMENT IX",
    "CLEMENT X",
    "INNOCENT XI",
    "ALEXANDRE VIII",
    "INNOCENT XII",
}

PERIOD_DISPLAY = {
    "CLEMENT VIII": "Clement VIII",
    "PAUL V": "Paul V",
    "GREGOIRE XV": "Grégoire XV",
    "URBAIN VIII": "Urbain VIII",
    "INNOCENT X": "Innocent X",
    "ALEXANDRE VII": "Alexandre VII",
    "CLEMENT IX": "Clément IX",
    "CLEMENT X": "Clément X",
    "INNOCENT XI": "Innocent XI",
    "ALEXANDRE VIII": "Alexandre VIII",
    "INNOCENT XII": "Innocent XII",
}

# Coordinates are deliberately curated, not automatically geocoded. Regional
# labels use an approximate center and are identified as generalized in the UI.
# Any unlisted source label remains searchable but unmapped pending review.
PLACE_AUTHORITY = {
    "Constantinople": ("Istanbul", 41.0082, 28.9784, "city", "high", "Historical city name"),
    "Constantinople (bisantinus)": ("Istanbul", 41.0082, 28.9784, "city", "high", "Historical city name"),
    "Alger": ("Algiers", 36.7538, 3.0588, "city", "high", "French historical label"),
    "Coron": ("Koroni", 36.7956, 21.9572, "city", "high", "Historical Venetian/French label"),
    "Tunis": ("Tunis", 36.8065, 10.1815, "city", "high", "Modern name unchanged"),
    "Smyrne": ("İzmir", 38.4237, 27.1428, "city", "high", "Historical city name"),
    "Mostar": ("Mostar", 43.3438, 17.8078, "city", "high", "Modern name unchanged"),
    "Anatolie": ("Anatolia, Turkey", 39.0, 35.0, "region", "medium", "Approximate regional center"),
    "Castronovo": ("Herceg Novi", 42.4572, 18.5315, "city", "medium", "Identification follows the explicit Castronovo (Herzegnovi) variant in the source"),
    "Castronovo (Herzegnovi)": ("Herceg Novi", 42.4572, 18.5315, "city", "high", "Modern identification supplied in source"),
    "Rhodes": ("Rhodes", 36.4349, 28.2176, "island/city", "high", "Mapped to Rhodes city"),
    "Tripoli": ("Tripoli, Libya", 32.8872, 13.1913, "city", "medium", "Distinguished from Tripolis, Syrie"),
    "Tripoli Barbari": ("Tripoli, Libya", 32.8872, 13.1913, "city", "high", "North African Tripoli"),
    "Dulcigno": ("Ulcinj", 41.9294, 19.2244, "city", "high", "Historical city name"),
    "Dalmatie": ("Dalmatia, Croatia", 43.5, 16.5, "region", "medium", "Approximate regional center"),
    "Nauplie": ("Nafplio", 37.5673, 22.8016, "city", "high", "Historical French name"),
    "Chypre": ("Cyprus", 35.1264, 33.4299, "island", "high", "Island centroid"),
    "Chios": ("Chios", 38.3676, 26.1358, "island/city", "high", "Mapped to Chios city"),
    "Santa Maura": ("Lefkada", 38.8334, 20.7069, "island", "high", "Historical island name"),
    "Biserte": ("Bizerte", 37.2746, 9.8739, "city", "high", "Historical spelling"),
    "Belgrade": ("Belgrade", 44.7866, 20.4489, "city", "high", "Modern name unchanged"),
    "Caramanie": ("Karaman region, Turkey", 37.1811, 33.2150, "region", "medium", "Approximate regional center"),
    "Clissa": ("Klis", 43.5600, 16.5222, "city", "high", "Historical name"),
    "Mer Noire": ("Black Sea", 43.0, 35.0, "region", "medium", "Approximate sea center"),
    "Salonique": ("Thessaloniki", 40.6401, 22.9444, "city", "high", "Historical French name"),
    "Negroponte": ("Chalcis, Euboea", 38.4625, 23.5950, "city/island", "medium", "Mapped to Chalcis, principal city of historical Negroponte"),
    "Aleppe": ("Aleppo", 36.2021, 37.1343, "city", "high", "Historical French spelling"),
    "Metelino": ("Mytilene", 39.1067, 26.5553, "city", "high", "Historical name"),
    "Mitellino": ("Mytilene", 39.1067, 26.5553, "city", "high", "Spelling variant"),
    "Romanie": ("Rumelia", 42.0, 24.0, "region", "medium", "Approximate historical regional center"),
    "Roumelie": ("Rumelia", 42.0, 24.0, "region", "medium", "Approximate historical regional center"),
    "Modon": ("Methoni", 36.8190, 21.7050, "city", "high", "Historical name"),
    "Navarino": ("Pylos", 36.9134, 21.6964, "city", "high", "Historical name"),
    "Damas": ("Damascus", 33.5138, 36.2765, "city", "high", "French historical label"),
    "Adrianople": ("Edirne", 41.6771, 26.5557, "city", "high", "Historical city name"),
    "Le Caire": ("Cairo", 30.0444, 31.2357, "city", "high", "French historical label"),
    "Moree": ("Peloponnese, Greece", 37.35, 22.35, "region", "medium", "Approximate historical regional center"),
    "Bosnie": ("Bosnia and Herzegovina", 44.1, 17.8, "region", "medium", "Approximate regional center"),
    "Gabella, Dalmatie": ("Gabela, Bosnia and Herzegovina", 43.0642, 17.6969, "city", "medium", "Historical regional attribution retained"),
    "Bone": ("Annaba", 36.9, 7.7667, "city", "high", "Historical city name"),
    "Hippo": ("Annaba", 36.9, 7.7667, "city", "high", "Mapped to ancient Hippo Regius/modern Annaba"),
    "Hippo, Africa": ("Annaba", 36.9, 7.7667, "city", "high", "Mapped to ancient Hippo Regius/modern Annaba"),
    "Athenes": ("Athens", 37.9838, 23.7275, "city", "high", "French historical label"),
    "Buda (Hongrie)": ("Budapest", 47.4979, 19.0402, "city", "high", "Historical Buda within modern Budapest"),
    "Tripolis, Syrie": ("Tripoli, Lebanon", 34.4333, 35.8333, "city", "high", "Levantine Tripoli"),
    "Valona": ("Vlorë", 40.4661, 19.4914, "city", "high", "Historical city name"),
    "Ablona": ("Vlorë", 40.4661, 19.4914, "city", "high", "Historical spelling variant"),
    "Aglona (Ablona?)": ("Vlorë", 40.4661, 19.4914, "city", "medium", "Tentative source identification retained"),
    "Mauritanie": ("Maghreb", 34.0, 1.0, "region", "low", "Generalized historical regional label; not modern Mauritania"),
    "Syrie": ("Syria", 35.0, 38.0, "region", "medium", "Approximate regional center"),
    "Samos": ("Samos", 37.7548, 26.9778, "island", "high", "Island centroid"),
    "Asie Mineure": ("Anatolia, Turkey", 39.0, 35.0, "region", "medium", "Approximate regional center"),
    "Bassora": ("Basra", 30.5085, 47.7804, "city", "high", "Historical French spelling"),
    "Hongrie": ("Hungary", 47.1625, 19.5033, "region", "medium", "Country centroid"),
    "Ubdina, Illiria": ("Udbina, Croatia", 44.5306, 15.7656, "city", "medium", "Historical spelling"),
    "Candia": ("Heraklion, Crete", 35.3387, 25.1442, "city", "high", "Historical city name"),
    "Sarai, Bosnie": ("Sarajevo", 43.8563, 18.4131, "city", "high", "Historical name"),
    "Mistra": ("Mystras", 37.0733, 22.3700, "city", "high", "Historical site"),
    "Knin": ("Knin", 44.0406, 16.1962, "city", "high", "Modern name unchanged"),
    "Sofia": ("Sofia", 42.6977, 23.3219, "city", "high", "Modern name unchanged"),
    "Sophia": ("Sofia", 42.6977, 23.3219, "city", "high", "Spelling variant"),
    "Pergame": ("Bergama", 39.1207, 27.1805, "city", "high", "Historical French name"),
    "Bursa": ("Bursa", 40.1950, 29.0600, "city", "high", "Modern name unchanged"),
    "Brussa": ("Bursa", 40.1950, 29.0600, "city", "high", "Historical spelling"),
    "Damiette": ("Damietta", 31.4175, 31.8144, "city", "high", "Historical French name"),
    "Saida": ("Sidon", 33.5606, 35.3758, "city", "high", "Historical Arabic/French label"),
    "Nicosia Chypre": ("Nicosia, Cyprus", 35.1856, 33.3823, "city", "high", "Modern city and country"),
    "Gallipoli": ("Gelibolu", 40.4093, 26.6708, "city", "high", "Historical city name"),
    "Tremisena in Barbaria": ("Tlemcen", 34.8783, -1.3150, "city", "high", "Historical Latin label"),
    "Scutari": ("Shkodër or Üsküdar", None, None, "ambiguous", "low", "Ambiguous historical label; intentionally unmapped"),
    "Albanie": ("Albania", 41.1533, 20.1683, "region", "medium", "Country centroid"),
    "Ethiopie": ("Ethiopia", 9.1450, 40.4897, "region", "medium", "Country centroid; historical extent may differ"),
    "Africa": ("Africa", 9.0, 20.0, "region", "low", "Very broad generalized label"),
    "Numidia": ("Northern Algeria", 36.0, 6.5, "region", "low", "Approximate historical region"),
}

ROMAN_MONTH = {"I": 1, "II": 2, "III": 3, "IV": 4, "V": 5, "VI": 6,
               "VII": 7, "VIII": 8, "IX": 9, "X": 10, "XI": 11, "XII": 12}
DATE_RE = re.compile(r"^(\d{4})\s+([IVX]+)\.(\d{1,2})\.?$")
YEAR_RE = re.compile(r"^(\d{4})(?:\.0)?$")


def normalize_text(value: str) -> str:
    value = unicodedata.normalize("NFKC", value or "")
    return re.sub(r"\s+", " ", value).strip()


def read_rows(path: Path) -> list[dict[str, str]]:
    with ZipFile(path) as archive:
        shared_root = ET.fromstring(archive.read("xl/sharedStrings.xml"))
        shared = [
            "".join((t.text or "") for t in item.iter(f"{{{MAIN_NS}}}t"))
            for item in shared_root.findall("m:si", NS)
        ]
        sheet = ET.fromstring(archive.read("xl/worksheets/sheet1.xml"))
        output = []
        for row in sheet.findall(".//m:sheetData/m:row", NS):
            values: dict[str, str] = {}
            for cell in row.findall("m:c", NS):
                match = re.match(r"[A-Z]+", cell.attrib["r"])
                if not match:
                    continue
                column = match.group(0)
                raw = cell.find("m:v", NS)
                value = ""
                if raw is not None:
                    value = shared[int(raw.text)] if cell.attrib.get("t") == "s" else (raw.text or "")
                elif cell.attrib.get("t") == "inlineStr":
                    value = "".join((t.text or "") for t in cell.iter(f"{{{MAIN_NS}}}t"))
                values[column] = normalize_text(value)
            if any(values.get(col) for col in "ABCDE"):
                output.append({"row": int(row.attrib["r"]), **values})
        return output


def parse_date(source_text: str) -> dict[str, object]:
    match = DATE_RE.match(source_text)
    if match:
        year, roman_month, day = match.groups()
        month = ROMAN_MONTH.get(roman_month)
        if month is None:
            raise ValueError(f"Unrecognized Roman month in {source_text!r}")
        parsed = date(int(year), month, int(day))
        return {"iso": parsed.isoformat(), "year": parsed.year, "precision": "day"}
    match = YEAR_RE.match(source_text)
    if match:
        year = int(match.group(1))
        return {"iso": f"{year:04d}-01-01", "year": year, "precision": "year"}
    raise ValueError(f"Unrecognized date format: {source_text!r}")


def build(source: Path, destination: Path) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    rows = read_rows(source)
    current_heading = "TABLEAU ANNEXE"
    preceding_date = ""
    records: list[dict[str, object]] = []

    for row in rows:
        if row["row"] == 1:
            continue
        marker = row.get("A", "")
        if marker in HEADINGS:
            current_heading = marker
            continue
        if not row.get("B") and not row.get("E"):
            continue

        explicit_date = marker
        if explicit_date:
            preceding_date = explicit_date
            date_basis = "explicit"
        else:
            if not preceding_date:
                raise ValueError(f"Row {row['row']} has no date to inherit")
            date_basis = "inherited"
        effective_date = preceding_date
        parsed = parse_date(effective_date)

        if current_heading == "TABLEAU ANNEXE":
            # All eight introductory entries resolve to 1600, within Clement VIII's
            # 1592–1605 pontificate. The source does not state this heading, so the
            # period is tagged as inferred rather than documentary.
            if parsed["year"] != 1600:
                raise ValueError(f"Unexpected Tableau annexe year at row {row['row']}: {parsed['year']}")
            papal_key = "CLEMENT VIII"
            papal_basis = "inferred_from_date"
            source_section = "TABLEAU ANNEXE"
        else:
            papal_key = current_heading
            papal_basis = "source_section_heading"
            source_section = current_heading

        origin = row.get("D", "")
        has_origin = bool(origin and origin.upper() != "N/A")
        authority = PLACE_AUTHORITY.get(origin) if has_origin else None
        modern, lat, lon, location_type, confidence, note = authority if authority else ("", None, None, "unresolved" if has_origin else "none", "unreviewed" if has_origin else "not_applicable", "Origin absent in source" if not has_origin else "Awaiting historical-place review")
        if has_origin and modern and modern.casefold() != origin.casefold():
            origin_display = f"{origin} ({modern})"
        else:
            origin_display = origin if has_origin else "Not recorded"

        records.append({
            "id": f"NA-{len(records)+1:04d}",
            "sourceRow": row["row"],
            "originalName": row.get("B", "") or "Not recorded",
            "baptismalName": row.get("E", "") or "Not recorded",
            "placeOfOrigin": origin if has_origin else "",
            "placeOfOriginDisplay": origin_display,
            "modernPlace": modern,
            "age": row.get("C", "") if row.get("C", "").upper() != "N/A" else "Not recorded",
            "dateSource": explicit_date,
            "dateDisplay": effective_date,
            "dateIso": parsed["iso"],
            "dateYear": parsed["year"],
            "datePrecision": parsed["precision"],
            "dateBasis": date_basis,
            "papalPeriod": PERIOD_DISPLAY[papal_key],
            "papalPeriodSource": source_section,
            "papalPeriodBasis": papal_basis,
            "latitude": lat,
            "longitude": lon,
            "locationType": location_type,
            "geocodingConfidence": confidence,
            "locationReviewNote": note,
            "hasOrigin": has_origin,
            "isMapped": lat is not None and lon is not None,
        })

    if len(records) != 781:
        raise ValueError(f"Expected 781 person records, found {len(records)}")

    papal_counts = Counter(record["papalPeriod"] for record in records)
    date_basis_counts = Counter(record["dateBasis"] for record in records)
    location_counts = Counter(
        "mapped" if record["isMapped"] else "unresolved" if record["hasOrigin"] else "no_origin"
        for record in records
    )

    # Complete public CSV: preserve the original Date cell exactly (including
    # blanks), then add the inherited numeric Year and transparent derived fields.
    csv_fields = [
        "Record ID", "Source Row", "Date", "Year", "Effective Date", "Date ISO",
        "Date Precision", "Date Status", "Original Name", "Age", "Place of Origin",
        "Baptismal Name", "Papal Period", "Papal Period Source", "Papal Period Basis",
        "Modern Place Name", "Place of Origin Display", "Latitude", "Longitude",
        "Location Type", "Location Status", "Geocoding Confidence",
        "Location Review Note", "Source",
    ]
    with (destination / "north-african-captives-complete.csv").open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=csv_fields)
        writer.writeheader()
        for record in records:
            location_status = "mapped" if record["isMapped"] else "awaiting review" if record["hasOrigin"] else "no recorded origin"
            writer.writerow({
                "Record ID": record["id"],
                "Source Row": record["sourceRow"],
                "Date": record["dateSource"],
                "Year": record["dateYear"],
                "Effective Date": record["dateDisplay"],
                "Date ISO": record["dateIso"],
                "Date Precision": record["datePrecision"],
                "Date Status": record["dateBasis"],
                "Original Name": record["originalName"],
                "Age": record["age"],
                "Place of Origin": record["placeOfOrigin"],
                "Baptismal Name": record["baptismalName"],
                "Papal Period": record["papalPeriod"],
                "Papal Period Source": record["papalPeriodSource"],
                "Papal Period Basis": record["papalPeriodBasis"],
                "Modern Place Name": record["modernPlace"],
                "Place of Origin Display": record["placeOfOriginDisplay"],
                "Latitude": record["latitude"],
                "Longitude": record["longitude"],
                "Location Type": record["locationType"],
                "Location Status": location_status,
                "Geocoding Confidence": record["geocodingConfidence"],
                "Location Review Note": record["locationReviewNote"],
                "Source": f"{SOURCE_TITLE}, {record['dateDisplay']}",
            })

    origin_counts = Counter(record["placeOfOrigin"] for record in records if record["hasOrigin"])
    authority_rows = []
    for label in sorted(origin_counts, key=str.casefold):
        entry = PLACE_AUTHORITY.get(label)
        if entry:
            modern, lat, lon, kind, confidence, note = entry
            status = "reviewed" if lat is not None else "ambiguous_unmapped"
        else:
            modern, lat, lon, kind, confidence, note = "", None, None, "unresolved", "unreviewed", "Awaiting historical-place review"
            status = "needs_review"
        authority_rows.append({
            "original_label": label,
            "normalized_label": normalize_text(label).casefold(),
            "record_count": origin_counts[label],
            "modern_label": modern,
            "latitude": lat,
            "longitude": lon,
            "location_type": kind,
            "geocoding_confidence": confidence,
            "review_status": status,
            "reviewer_note": note,
        })

    with (destination / "place-authority.csv").open("w", encoding="utf-8-sig", newline="") as handle:
        fields = list(authority_rows[0])
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(authority_rows)

    marker_groups: dict[str, dict[str, object]] = {}
    for record in records:
        if not record["isMapped"]:
            continue
        key = f"{record['latitude']:.4f},{record['longitude']:.4f}"
        group = marker_groups.setdefault(key, {
            "key": key,
            "latitude": record["latitude"], "longitude": record["longitude"],
            "labels": [], "modernPlaces": [], "recordIds": [],
            "locationType": record["locationType"],
        })
        if record["placeOfOrigin"] not in group["labels"]:
            group["labels"].append(record["placeOfOrigin"])
        if record["modernPlace"] and record["modernPlace"] not in group["modernPlaces"]:
            group["modernPlaces"].append(record["modernPlace"])
        group["recordIds"].append(record["id"])
    markers = sorted(marker_groups.values(), key=lambda item: (-len(item["recordIds"]), item["key"]))

    payload = {
        "meta": {
            "title": "Captives from North Africa and the Ottoman World",
            "version": "0.3.1",
            "recordCount": len(records),
            "yearMin": min(record["dateYear"] for record in records),
            "yearMax": max(record["dateYear"] for record in records),
            "generatedBy": "scripts/prepare_data.py",
            "dateRule": "Blank date cells inherit the preceding explicit source date and are flagged inherited.",
            "papalRule": "Source headings govern following records; the eight 1600 Tableau annexe records are assigned Clement VIII and flagged inferred from chronology.",
        },
        "stats": {
            "papalPeriods": dict(sorted(papal_counts.items())),
            "dateBasis": dict(sorted(date_basis_counts.items())),
            "locations": dict(sorted(location_counts.items())),
            "distinctOriginLabels": len(origin_counts),
        },
        "records": records,
        "markers": markers,
    }
    (destination / "app-data.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    # A JavaScript copy allows the prepared package to load its records without a
    # fetch request. This makes the map more reliable on GitHub Pages and also
    # keeps the record interface available when index.html is opened directly.
    (destination / "app-data.js").write_text(
        "window.NORTH_AFRICAN_CAPTIVES_DATA = "
        + json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
        + ";\n",
        encoding="utf-8",
    )
    (destination / "build-report.json").write_text(json.dumps({
        "records": len(records),
        "explicitDates": date_basis_counts["explicit"],
        "inheritedDates": date_basis_counts["inherited"],
        "papalPeriodCounts": dict(papal_counts),
        "mappedRecords": location_counts["mapped"],
        "unresolvedOriginRecords": location_counts["unresolved"],
        "noOriginRecords": location_counts["no_origin"],
        "distinctOriginLabels": len(origin_counts),
        "reviewedAuthorityLabels": sum(1 for row in authority_rows if row["review_status"] == "reviewed"),
        "ambiguousUnmappedLabels": sum(1 for row in authority_rows if row["review_status"] == "ambiguous_unmapped"),
        "needsReviewLabels": sum(1 for row in authority_rows if row["review_status"] == "needs_review"),
    }, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"Built {len(records)} records in {destination}")
    print(json.dumps(payload["stats"], ensure_ascii=False, indent=2))


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit("Usage: prepare_data.py SOURCE.xlsx DESTINATION_DATA_DIR")
    build(Path(sys.argv[1]), Path(sys.argv[2]))


if __name__ == "__main__":
    main()
