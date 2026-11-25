/* Captives from North Africa and the Ottoman World — v0.3.1.
   Static GitHub Pages application; no build step and no API key. */
(() => {
  "use strict";

  const COLORS = { city: "#a34a32", region: "#2d5e52" };
  const SOURCE_TITLE = "Le baptême des musulmans esclaves à Rome";
  const MAX_LISTED_RECORDS = 250;
  const PERIOD_ORDER = [
    "Clement VIII", "Paul V", "Grégoire XV", "Urbain VIII", "Innocent X",
    "Alexandre VII", "Clément IX", "Clément X", "Innocent XI", "Alexandre VIII", "Innocent XII",
  ];
  const state = {
    data: null,
    map: null,
    layers: {},
    selectedMarkerKey: null,
    lastFocus: null,
  };

  const el = (id) => document.getElementById(id);
  const controls = {
    search: el("record-search"),
    minYear: el("min-year"),
    maxYear: el("max-year"),
    minOutput: el("min-year-output"),
    maxOutput: el("max-year-output"),
    period: el("papal-period"),
  };

  function escapeHtml(value) {
    return String(value ?? "").replace(/[&<>'"]/g, (char) => ({
      "&": "&amp;", "<": "&lt;", ">": "&gt;", "'": "&#39;", '"': "&quot;",
    }[char]));
  }

  function normalize(value) {
    return String(value ?? "")
      .normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "")
      .toLocaleLowerCase()
      .replace(/\s+/g, " ")
      .trim();
  }

  function compactNumber(value) {
    return new Intl.NumberFormat("en", {
      notation: value >= 1000 ? "compact" : "standard",
      maximumFractionDigits: 1,
    }).format(value);
  }

  function debounce(fn, wait = 120) {
    let timer;
    return (...args) => {
      window.clearTimeout(timer);
      timer = window.setTimeout(() => fn(...args), wait);
    };
  }

  function activeMode() {
    return document.querySelector('input[name="map-mode"]:checked')?.value || "all";
  }

  function markerKey(record) {
    return record.isMapped ? `${Number(record.latitude).toFixed(4)},${Number(record.longitude).toFixed(4)}` : null;
  }

  function initializeMap() {
    if (typeof window.L === "undefined") return false;
    state.map = L.map("map", { preferCanvas: true, zoomControl: true, minZoom: 2, worldCopyJump: true })
      .setView([38, 20], 4);
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      maxZoom: 18,
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    }).addTo(state.map);
    L.control.scale({ imperial: false }).addTo(state.map);
    state.layers.marker = L.layerGroup().addTo(state.map);
    state.layers.highlight = L.layerGroup().addTo(state.map);
    window.addEventListener("load", () => state.map?.invalidateSize());
    return true;
  }

  function populatePeriodDropdown() {
    const counts = state.data.stats.papalPeriods;
    for (const period of PERIOD_ORDER) {
      if (!(period in counts)) continue;
      const option = document.createElement("option");
      option.value = period;
      option.textContent = `${period} (${counts[period].toLocaleString()})`;
      controls.period.append(option);
    }
  }

  function normalizedYearBounds() {
    let min = Number(controls.minYear.value);
    let max = Number(controls.maxYear.value);
    if (min > max) [min, max] = [max, min];
    controls.minOutput.value = String(min);
    controls.maxOutput.value = String(max);
    return { min, max };
  }

  function setYearRangeForPeriod(period) {
    const meta = state.data.meta;
    if (!period) {
      controls.minYear.value = meta.yearMin;
      controls.maxYear.value = meta.yearMax;
      return;
    }
    const years = state.data.records
      .filter((record) => record.papalPeriod === period)
      .map((record) => Number(record.dateYear))
      .filter(Number.isFinite);
    if (!years.length) return;
    controls.minYear.value = Math.min(...years);
    controls.maxYear.value = Math.max(...years);
  }

  function recordSearchText(record) {
    return normalize([
      record.originalName, record.baptismalName, record.placeOfOrigin,
      record.placeOfOriginDisplay, record.modernPlace, record.age,
      record.dateDisplay, record.dateYear, record.papalPeriod, record.id,
    ].join(" "));
  }

  function baseFilteredRecords() {
    const { min, max } = normalizedYearBounds();
    const query = normalize(controls.search.value);
    const period = controls.period.value;
    const mode = activeMode();
    return state.data.records.filter((record) => {
      if (record.dateYear < min || record.dateYear > max) return false;
      if (period && record.papalPeriod !== period) return false;
      if (mode === "mapped" && !record.isMapped) return false;
      if (mode === "no-origin" && record.hasOrigin) return false;
      return !query || recordSearchText(record).includes(query);
    });
  }

  function panelFilteredRecords(records) {
    if (!state.selectedMarkerKey) return records;
    return records.filter((record) => markerKey(record) === state.selectedMarkerKey);
  }

  function buildMarkerGroups(records) {
    const groups = new Map();
    for (const record of records) {
      if (!record.isMapped) continue;
      const key = markerKey(record);
      if (!groups.has(key)) groups.set(key, []);
      groups.get(key).push(record);
    }
    return groups;
  }

  function renderMap(records) {
    if (!state.map || !state.layers.marker) return;
    state.layers.marker.clearLayers();
    const groups = buildMarkerGroups(records);
    for (const [key, group] of groups) {
      const first = group[0];
      const labels = [...new Set(group.map((record) => record.placeOfOrigin))];
      const modern = [...new Set(group.map((record) => record.modernPlace).filter(Boolean))];
      const generalized = group.some((record) => /region|island|country|sea/i.test(record.locationType || ""));
      const radius = Math.min(24, 5 + Math.sqrt(group.length) * 1.1);
      const marker = L.circleMarker([first.latitude, first.longitude], {
        radius,
        color: "#fffdf8",
        weight: 1.7,
        fillColor: generalized ? COLORS.region : COLORS.city,
        fillOpacity: .88,
      }).addTo(state.layers.marker);
      const placeTitle = labels.join(" / ");
      marker.bindPopup(`
        <h3>${escapeHtml(placeTitle)}${modern.length ? ` (${escapeHtml(modern.join(" / "))})` : ""}</h3>
        <div class="popup-meta"><strong>${group.length.toLocaleString()}</strong> matching record${group.length === 1 ? "" : "s"}</div>
        <div class="popup-note">${generalized ? "Generalized regional or island reference." : "Reviewed origin point."} Selecting this point narrows the record list.</div>`);
      marker.bindTooltip(`${placeTitle}: ${group.length.toLocaleString()} record${group.length === 1 ? "" : "s"}`, { sticky: true });
      marker.on("click", () => {
        state.selectedMarkerKey = key;
        el("selection-chip").hidden = false;
        el("selection-label").textContent = `Origin: ${placeTitle}`;
        renderRecordList(panelFilteredRecords(baseFilteredRecords()));
      });
    }
  }

  function renderRecordList(records) {
    const container = el("record-list");
    container.replaceChildren();
    el("record-count").textContent = `${records.length.toLocaleString()} matching`;
    const limited = records.slice(0, MAX_LISTED_RECORDS);
    el("record-limit-note").textContent = records.length > MAX_LISTED_RECORDS
      ? `Showing the first ${MAX_LISTED_RECORDS.toLocaleString()} records. Refine the search, year range, Papal Period, or map selection to narrow the list.`
      : "Select a person to open the concise historical record.";

    if (!records.length) {
      const empty = document.createElement("div");
      empty.className = "empty-state";
      empty.textContent = "No records match the current filters.";
      container.append(empty);
      return;
    }

    const fragment = document.createDocumentFragment();
    for (const record of limited) {
      const button = document.createElement("button");
      button.type = "button";
      button.className = `record-card ${record.isMapped ? "mapped" : record.hasOrigin ? "unresolved" : "no-origin"}`;
      button.setAttribute("aria-label", `Open record for ${record.originalName} and ${record.baptismalName}`);

      const pair = document.createElement("span");
      pair.className = "name-pair";
      const original = document.createElement("span");
      original.className = "name-block";
      const originalLabel = document.createElement("small");
      originalLabel.textContent = "Original name";
      const originalValue = document.createElement("strong");
      originalValue.textContent = record.originalName;
      original.append(originalLabel, originalValue);

      const baptismal = document.createElement("span");
      baptismal.className = "name-block";
      const baptismalLabel = document.createElement("small");
      baptismalLabel.textContent = "Baptismal name";
      const baptismalValue = document.createElement("strong");
      baptismalValue.textContent = record.baptismalName;
      baptismal.append(baptismalLabel, baptismalValue);
      pair.append(original, baptismal);

      const meta = document.createElement("span");
      meta.className = "record-meta";
      const periodSuffix = record.papalPeriodBasis === "inferred_from_date" ? " (inferred)" : "";
      meta.textContent = `${record.placeOfOriginDisplay} · ${record.dateYear} · ${record.papalPeriod}${periodSuffix}`;
      button.append(pair, meta);
      button.addEventListener("click", () => openRecord(record, button));
      fragment.append(button);
    }
    container.append(fragment);
  }

  function updateStats(records) {
    const markerKeys = new Set();
    let mapped = 0;
    for (const record of records) {
      if (record.isMapped) {
        mapped += 1;
        markerKeys.add(markerKey(record));
      }
    }
    el("stat-records").textContent = compactNumber(records.length);
    el("stat-mapped").textContent = compactNumber(mapped);
    el("stat-locations").textContent = markerKeys.size.toLocaleString();
    el("stat-unmapped").textContent = compactNumber(records.length - mapped);
  }

  function render() {
    const records = baseFilteredRecords();
    renderMap(records);
    updateStats(records);
    renderRecordList(panelFilteredRecords(records));
  }

  function clearLocationSelection() {
    state.selectedMarkerKey = null;
    el("selection-chip").hidden = true;
    el("selection-label").textContent = "";
  }

  function resetAll() {
    const meta = state.data.meta;
    controls.search.value = "";
    controls.minYear.value = meta.yearMin;
    controls.maxYear.value = meta.yearMax;
    controls.period.value = "";
    document.querySelector('input[name="map-mode"][value="all"]').checked = true;
    clearLocationSelection();
    closeDetail();
    state.map?.closePopup();
    state.map?.setView([38, 20], 4);
    render();
  }

  function detailRow(label, value, note = "", flag = "") {
    const tr = document.createElement("tr");
    const th = document.createElement("th");
    th.scope = "row";
    th.textContent = label;
    const td = document.createElement("td");
    td.textContent = value || "Not recorded";
    if (flag) {
      const badge = document.createElement("span");
      badge.className = "method-flag";
      badge.textContent = flag;
      td.append(document.createElement("br"), badge);
    }
    if (note) {
      const small = document.createElement("small");
      small.className = "evidence-note";
      small.textContent = note;
      td.append(small);
    }
    tr.append(th, td);
    return tr;
  }

  function papalEvidence(record) {
    if (record.papalPeriodBasis === "inferred_from_date") {
      return {
        flag: "Inferred period",
        note: "The source places this person under Tableau annexe. Clement VIII is assigned from the 1600 effective date and remains marked as an inference.",
      };
    }
    return { flag: "", note: "" };
  }

  function sourceDetailRow(record) {
    const tr = document.createElement("tr");
    const th = document.createElement("th");
    th.scope = "row";
    th.textContent = "Source";
    const td = document.createElement("td");
    const title = document.createElement("em");
    title.textContent = SOURCE_TITLE;
    td.append(title, document.createTextNode(`, ${record.dateDisplay}`));
    tr.append(th, td);
    return tr;
  }

  function placeEvidence(record) {
    if (!record.hasOrigin) return "No place of origin is recorded; no map point is created.";
    if (!record.isMapped) return "A historical origin is recorded, but its identification remains unresolved or under review; it is intentionally left off the map.";
    if (/region|island|country|sea/i.test(record.locationType || "")) return "The point is a generalized regional or island reference, not a precise birthplace.";
    if (record.modernPlace && normalize(record.modernPlace) !== normalize(record.placeOfOrigin)) return "Historical wording appears first; the reviewed modern reference appears in parentheses.";
    return "";
  }

  function openRecord(record, trigger) {
    state.lastFocus = trigger || document.activeElement;
    if (state.layers.highlight) state.layers.highlight.clearLayers();
    if (state.map && record.isMapped) {
      const point = [record.latitude, record.longitude];
      L.circleMarker(point, {
        radius: 10, color: "#fff", weight: 3,
        fillColor: /region|island|country|sea/i.test(record.locationType || "") ? COLORS.region : COLORS.city,
        fillOpacity: 1,
      }).addTo(state.layers.highlight);
      state.map.setView(point, Math.max(state.map.getZoom(), 6));
    }

    el("detail-title").textContent = record.originalName;
    el("detail-subtitle").textContent = record.baptismalName;
    const content = el("detail-content");
    content.replaceChildren();
    const table = document.createElement("table");
    table.className = "detail-table";
    const papal = papalEvidence(record);
    table.append(
      detailRow("Original Name", record.originalName),
      detailRow("Baptismal Name", record.baptismalName),
      detailRow("Place of Origin", record.placeOfOriginDisplay, placeEvidence(record)),
      detailRow("Age", record.age),
      detailRow("Date", String(record.dateYear)),
      sourceDetailRow(record),
      detailRow("Papal Period", record.papalPeriod, papal.note, papal.flag),
    );
    content.append(table);
    const panel = el("detail-panel");
    panel.classList.add("open");
    panel.setAttribute("aria-hidden", "false");
    el("close-detail").focus();
  }

  function closeDetail() {
    const panel = el("detail-panel");
    panel.classList.remove("open");
    panel.setAttribute("aria-hidden", "true");
    state.layers.highlight?.clearLayers();
    if (state.lastFocus && typeof state.lastFocus.focus === "function") state.lastFocus.focus();
  }

  function openHelp() {
    const dialog = el("help-dialog");
    if (!dialog.open) dialog.showModal();
  }

  function closeHelp() {
    el("help-dialog").close();
    try { localStorage.setItem("northAfricanCaptivesGuideSeenV02", "yes"); } catch (_) { /* storage may be blocked */ }
  }

  function bindControls() {
    const rerender = debounce(() => {
      clearLocationSelection();
      render();
    }, 90);
    controls.search.addEventListener("input", rerender);
    controls.minYear.addEventListener("input", rerender);
    controls.maxYear.addEventListener("input", rerender);
    controls.period.addEventListener("change", () => {
      clearLocationSelection();
      setYearRangeForPeriod(controls.period.value);
      render();
    });
    document.querySelectorAll('input[name="map-mode"]').forEach((input) => input.addEventListener("change", rerender));
    el("clear-selection").addEventListener("click", resetAll);
    el("reset-filters").addEventListener("click", resetAll);
    el("close-detail").addEventListener("click", closeDetail);
    el("help-button").addEventListener("click", openHelp);
    el("close-help").addEventListener("click", closeHelp);
    el("finish-help").addEventListener("click", closeHelp);
    el("help-dialog").addEventListener("cancel", (event) => { event.preventDefault(); closeHelp(); });
    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape" && el("detail-panel").classList.contains("open")) closeDetail();
    });
  }

  function showError(message) {
    const box = el("map-error");
    box.hidden = false;
    box.textContent = message;
  }

  function start() {
    state.data = window.NORTH_AFRICAN_CAPTIVES_DATA || null;
    if (!state.data) {
      el("loading").hidden = true;
      showError("The prepared data file could not be loaded. Confirm that the data folder is beside index.html.");
      return;
    }

    const meta = state.data.meta;
    for (const range of [controls.minYear, controls.maxYear]) {
      range.min = meta.yearMin;
      range.max = meta.yearMax;
      range.step = 1;
    }
    controls.minYear.value = meta.yearMin;
    controls.maxYear.value = meta.yearMax;
    populatePeriodDropdown();
    bindControls();

    if (!initializeMap()) {
      showError("The map library could not be loaded. The record list and CSV download remain available; check the internet connection or content-blocking settings for the map.");
    }
    render();
    el("loading").hidden = true;
    try {
      if (!localStorage.getItem("northAfricanCaptivesGuideSeenV02")) window.setTimeout(openHelp, 400);
    } catch (_) { /* storage may be blocked */ }
  }

  start();
})();
