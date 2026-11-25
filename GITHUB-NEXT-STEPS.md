# GitHub next steps — North African/Ottoman map v0.3.1

## Replace the repository files

1. Download and extract `north-african-captives-map-v0.3.1.zip`.
2. Open the repository that will host this companion map.
3. Select **Add file → Upload files**.
4. Upload the **contents** of the extracted folder, not the outer folder.
5. Confirm that `index.html`, `app.js`, and `styles.css` appear at the repository root and that the `data` and `scripts` folders are present.
6. Replace files with matching names.
7. Commit with a message such as `Publish North African captives map v0.3.1`.

Do not upload the source workbook unless you intend to make it public. The prepared map does not need the workbook at runtime.

## Publish or refresh GitHub Pages

1. Open **Settings → Pages** in the repository.
2. Under **Build and deployment**, choose **Deploy from a branch**.
3. Select the `main` branch and `/ (root)` folder.
4. Save and wait for the deployment under **Actions** to receive a green check.
5. Return to **Settings → Pages** and select **Visit site**.
6. Hard-refresh the site if an older version appears.

## Five-minute review

1. Confirm the OpenStreetMap basemap and origin markers appear.
2. Select **How to use this map** and verify the guide opens.
3. Move both handles on the single year timeline.
4. Choose one **Papal Period** and confirm both timeline handles move to that period's earliest and latest represented years.
5. Search an original name and a baptismal name.
6. Open a record and confirm Date shows only a year while Source directly beneath it shows the italicized title and complete date notation.
7. Select **No recorded origin** and verify 92 records are available before applying other filters.
8. Select a map location, change several filters, then use the location X and confirm the location name, search, Papal Period, timeline, and location mode all reset.
9. Download the complete CSV and confirm that it contains 781 records, an original Date column, and a numeric Year column.
10. Test at 200% browser zoom and on a phone-width window.

## If the map area is blank

- Confirm that `data/app-data.js` is uploaded beside `data/app-data.json`.
- Confirm that the browser can reach `unpkg.com` and OpenStreetMap tile servers.
- Disable an overly strict content blocker for the site and refresh.
- The records and CSV should remain available even if the basemap library or tiles are blocked.
