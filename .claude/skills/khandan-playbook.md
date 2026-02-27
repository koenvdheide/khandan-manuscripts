# Khandan Search Playbook

Procedural reference for searching portal.yek.gov.tr for manuscripts written by Sultan Muhammad Khandan (خندان). Used by `khandan-search` and `colophon-verifier` agents.

## Portal Overview

**URL**: <https://portal.yek.gov.tr>
**Advanced search**: <https://portal.yek.gov.tr/works/advancedsearch/full>
**Registration**: Free, required for full access
**Language**: Turkish
**Coverage**: ~600,000 manuscript records across 252 collections in Turkey

**IMPORTANT — yazmalar.gov.tr = YEK**: The domains portal.yek.gov.tr and yazmalar.gov.tr resolve to the **same system**. Do NOT search yazmalar.gov.tr separately — it is not a distinct portal. Any search done in YEK already covers yazmalar.gov.tr.

**Topkapi Palace Library in YEK**: Topkapi (TSMK) records **are** in YEK. However, Topkapi manuscripts have **no digitized images** — colophon-verifier cannot confirm attributions from Topkapi records. Sessions 1–3 (exhaustive person-field searches) found zero Topkapi records attributed to Khandan.

## Authentication

The YEK portal requires login. Credentials are stored in `.env` (gitignored) in the project root:

```env
YEK_USERNAME=your_email_or_tc_no
YEK_PASSWORD=your_password
```

### Auto-login procedure

Before executing any search or navigation, check if the browser session is already authenticated:

1. Take a `browser_snapshot` after navigating to <https://portal.yek.gov.tr>. Look for a logout indicator in the header ("Çıkış Yap", a user name, or a member dashboard element). If found, the session is active — skip login.
2. If not logged in:

   a. Read credentials from `.env` using Bash:

   ```bash
   grep "^YEK_USERNAME" .env | sed 's/.*= *//'
   grep "^YEK_PASSWORD" .env | sed 's/.*= *//'
   ```

   Note: The `.env` file uses spaces around `=` (e.g. `YEK_USERNAME = value`), so `cut -d= -f2-` does not work — use `sed 's/.*= *//'` instead.

   b. Click the "Giriş" (login) link in the portal header, or navigate directly to the login page.
   c. Fill the login form using `browser_fill_form` with the username and password.
   d. Click the submit button ("Giriş Yap").
   e. Take a `browser_snapshot` to confirm login succeeded (look for user name or "Çıkış Yap" in the header).
   f. If login fails, stop and report the error to the user — do not retry with the same credentials.

## Search Interface

### Form structure

The advanced search form has:

1. A **field selector** dropdown (42 fields available)
2. An **operator** dropdown (İçeren = contains, Eşit = equals)
3. A **value** text input
4. A **search** button (Ara)
5. Additional filter rows can be added ("+Kural Ekle") for AND-combined searches

### Key fields for calligrapher attribution

| Field label (Turkish) | Best for |
| --- | --- |
| Nüshayla ilgili kişiler | Primary field for calligrapher identity. Includes müstensih, hattat, müzehhip, mücellid, vâkıf, mütemellik roles. |
| İstinsah kaydı (Arap harfli) | Colophon text verbatim in Arabic script. Search for signature kernels here. Separate from seals. |
| Mühürler | Ownership and waqf seals only. Separate from colophon text. |
| Genel Notlar | Free-text descriptions. Use as fallback with higher expected false positive rate. |
| Yazı Türü | Script type — use as precision multiplier (nestalik, talik) |
| Dili | Language — use to narrow (Farsça, Türkçe, Arapça) |
| İstinsah Tarihi | Date of copying — use to filter to 915–992 AH / 1500–1584 CE |

### İçeren operator behavior (critical)

The İçeren (contains) operator **tokenizes multi-word queries** and matches each word independently anywhere in the field:

- ✅ Catches variant word orders (e.g., "سلطان محمد خندان" also matches "محمد سلطان خندان")
- ⚠️ Hyphens tokenize heavily — **never search hyphenated forms**
- ✅ Diacritics are normalized server-side — one form suffices, do not rotate
- ⚠️ Short common words in Arabic may match as parts of other words — read full field text to confirm
- ⚠️ "خندان" alone will match "Handan" as a Turkish name in Latin-transliterated records

## Term Tiers

### Tier 1 — Highest precision (start here)

| Term | Script | Best field | Expected FP rate |
| --- | --- | --- | --- |
| `سلطان محمد خندان` | Arabic | Nüshayla ilgili kişiler | ~2–5% |
| `سلطان محمد خندان` | Arabic | İstinsah kaydı (Arap harfli) | ~5% |

### Tier 2 — Good precision (use if Tier 1 sparse)

| Term | Script | Best field | Expected FP rate |
| --- | --- | --- | --- |
| `محمد خندان` | Arabic | Nüshayla ilgili kişiler | ~10–15% |
| `خندان هروی` | Arabic | Nüshayla ilgili kişiler | ~10% |
| `مولانا خندان` | Arabic | Nüshayla ilgili kişiler | ~15% |
| `سلطان محمد خندان هروی` | Arabic | Genel Notlar | ~5% |

### Tier 3 — Colophon kernels (search in İstinsah kaydı (Arap harfli))

| Term | Arabic | Notes |
| --- | --- | --- |
| `كتبه خندان` | كتبه خندان | "Written by Khandan" — direct colophon phrase |
| `العبد خندان` | العبد خندان | "The servant Khandan" — humility colophon formula |
| `حرره خندان` | حرره خندان | "Corrected/written by Khandan" |
| `فقیر خندان` | فقیر خندان | "The poor one Khandan" — Persian humility formula |

### Tier 4 — Arabic script alone (use with filter only)

| Term | Notes |
| --- | --- |
| `خندان` | Many false positives. Use ONLY combined with: (a) Nüshayla ilgili kişiler field, AND (b) date filter 900–1000 AH, AND (c) script filter nestalik/talik |

### Tier 5 — Latin transliterations (use if Arabic-field searches sparse)

| Term | Notes |
| --- | --- |
| `Sultan Muhammed Handan` | Turkish transliteration style |
| `Sultan Muhammed Hândân` | With circumflex |
| `Khandan` | English transliteration |
| `Khondan` | Alternate English romanization — test in Nüshayla ilgili kişiler |
| `Handan` | Turkish form — very high FP rate; use only in Nüshayla ilgili kişiler |

## Search Strategy Protocols

### Protocol A: Standard survey (first session)

1. Tier 1: `سلطان محمد خندان` in Nüshayla ilgili kişiler
2. Tier 1: `سلطان محمد خندان` in İstinsah kaydı (Arap harfli)
3. Tier 3 colophon kernels in İstinsah kaydı (Arap harfli)
4. Tier 2: `محمد خندان` and `خندان هروی` in Nüshayla ilgili kişiler
5. Tier 5 Latin variants in Nüshayla ilgili kişiler

### Protocol B: Expanding sparse results

If Protocol A yields fewer than 5 genuine results:

1. Add Tier 2 terms in Genel Notlar
2. Add Tier 4 `خندان` in Nüshayla ilgili kişiler (without additional filter first, then with date filter)
3. Add Tier 5 Latin variants in Genel Notlar

**Note (confirmed 2026-02-26):** Steps 1, 3, and Tier 4 were executed in Session 3 with 0 new genuine results. Arabic Tier 2 terms return 0 hits in Genel Notlar (field not indexed for Arabic script). Latin variants in Genel Notlar produce only tokenization false positives. Tier 4 خندان alone in Nüshayla ilgili kişiler returns only the 2 known manuscripts + Khandanzade instances.

### Protocol C: Precision multiplier

Combine person-name term with script or language filter (AND rules) to reduce false positives:

- Add row: Yazı Türü İçeren `Nesta` — partial match for "Nesta'lîk" (do NOT use plain "nestalik" — returns 0 due to apostrophe+accent in YEK's controlled term)
- Add row: Dili İçeren `Farsça` — many of his works are Persian literary texts
- Add row: date filter 900–1000 AH

### Protocol D: Avoiding duplicate work

Always check MEMORY.md Search History before executing a search. Skip any term × field combination already searched in a previous session. Deduplicate results using YEK record ID as the primary key.

## False Positive Detection Rules

| Pattern | If found | Action |
| --- | --- | --- |
| Person listed as vâkıf, mütemellik, mütercim, şâriḥ — not müstensih or hattat | Role mismatch | Mark false positive |
| "Handan" context is a female Turkish given name (patron, owner, dedicatee) | Turkish name, not calligrapher | Mark false positive |
| `نور` (light/nur) where you expected `خندان` (smiling/khandan) | Likely Sultan Muhammad Nūr | Mark `disambiguation_needed: "Sultan Muhammad Nur"` |
| Name includes `خندان زاده` / Khandanzāde ("son of Khandan") | Later family name; tokenizer matches خندان independently. Confirmed YEK 143215 (Süleymaniye 00143, 1160 AH / 1747 CE, copyist = Ahmad b. al-Hajj Muhammad al-Khandanzāde) | Mark false positive |
| Manuscript dated firmly before 900 AH or after 1000 AH | Outside activity window | Flag as `date_mismatch`; still record |
| Script type recorded as nesih, sülüs, muhakkak, reyhânî (not nastaʿlīq/taʿlīq) | Unlikely Khandan | Flag as `script_mismatch`; still record |
| "خندان" as adjective in a phrase (e.g., "روی خندان", "چهره خندان") | Adjectival use | Mark false positive |
| Modern administrative document, vakıfname, or non-literary genre | Context incompatible | Mark false positive |
| Latin-script "Handan" result where person is author, patron, or owner | Role mismatch | Mark false positive |
| Multiple persons listed in Nüshayla ilgili kişiler; `خندان` matches a non-scribe role | Role mismatch | Mark false positive after reading full text |

## Navigating the YEK Viewer for Colophon Access

### Accessing digitized images

From a manuscript detail page, look for:

- "Görüntü" button or link
- Viewer opens in a modal or new pane (OpenSeadragon-based)

### Page navigation

- The viewer shows "X / Y" page counter (current page / total pages)
- Navigate to a specific page by clicking the page number input field and typing the page number, then pressing Enter
- Or use next/previous arrow buttons for small adjustments
- Use the last-page button (if present) to jump to the end

### Colophon capture strategy

- Target last 10 pages (Y−9 through Y) for manuscripts with Y > 20
- Target last half for short manuscripts (Y ≤ 20)
- The very last page is often a blank leaf or endpaper — start from Y−1 backward
- Take screenshots of all target pages before attempting to read — survey first, read second

### Screenshot filename convention

```text
{collection}_{shelfmark}_p{page:03d}_{method}.png
```

- `{method}`: `iiif` for IIIF downloads, `view` for viewer captures
- Save to: `corpus/colophon_screenshots/`
- Example: `suleymaniye_hafiz_ahmed_01234_p187_iiif.png`

### Portal reliability

Turkish government portals can be intermittently slow. If a page fails to load:

- Wait 5 seconds and retry once
- If viewer fails, try refreshing the detail page first

## IIIF Direct Image Access

The YEK portal uses IIIF Image API Level 2. Prefer IIIF for all analysis images — higher native resolution, no UI chrome.

### Image URL pattern

```text
https://portal.yek.gov.tr/iiif/webservice/ShowImage/{internal_iiif_id}/{page}/full/{size}/0/default.jpg
```

- `{internal_iiif_id}` — 13-digit zero-padded internal ID (e.g. `0000000660191`)
- `{page}` — 1-indexed page number
- `{size}` — `1600,` for 1600px width (minimum for text reading); `full` for native resolution; `90,` for thumbnails

### IIIF page numbers vs. viewer page numbers

**Critical**: The IIIF page number and the YEK viewer page number are **not always the same**. The viewer may display a page counter that is offset by ~2 from the true IIIF sequence (due to cover/endpaper images prepended to the IIIF manifest). Always verify colophon page identity by loading IIIF images directly — do not trust viewer page counter for IIIF URLs.

Example: For Arkeoloji Recaizade Ekrem Bey 00066, viewer page 146 ≈ IIIF page 147 (offset = 1–2 pages).

### Extracting the internal IIIF ID

The ID is not in the detail page HTML. Extract by intercepting the `get_manifesto_data` network request fired when the viewer button is clicked:

```js
async (page) => {
  const manuscripts = [
    { yekId: 177740, record: 'example_manuscript' },
    // add more as needed
  ];
  const ids = {};
  for (const m of manuscripts) {
    const captured = [];
    const handler = req => captured.push(req.url());
    page.on('request', handler);
    await page.goto(`https://portal.yek.gov.tr/works/detail/${m.yekId}`);
    captured.length = 0;
    await page.getByRole('link', { name: 'Görüntü' }).click();
    await page.waitForTimeout(5000);
    page.off('request', handler);
    const manifestUrl = captured.find(url => url.includes('get_manifesto_data'));
    const decoded = decodeURIComponent(manifestUrl);
    const match = decoded.match(/get_manifesto_data\/(\d+)\//i);
    ids[m.record] = match ? match[1] : 'REGEX_FAIL';
    await page.keyboard.press('Escape');
    await page.waitForTimeout(500);
  }
  return ids;
}
```

**Key notes:**

- Use `page.on('request')` not `page.waitForRequest()` — the manifest URL appears URL-encoded (`%2F`) inside the `app.html` iframe query string
- `decodeURIComponent` is required to decode the URL before regex matching
- Clear `captured` after `page.goto`, not before — captures only requests from the click
- 5-second wait needed for iframe to initiate its own network requests
- Store extracted IDs in the search JSON as `internal_iiif_id`

### IIIF ID fallback: byte-size probing

If network interception fails (e.g., the Görüntü button click does not fire a `get_manifesto_data` request in the captured window), use **byte-size probing** to find the IIIF ID:

1. Known IIIF IDs for this institution cluster near each other numerically. Start from a known ID (e.g., Arkeoloji 00153 = `0000000665118`) and scan ±500 in steps of 1.
2. For each candidate ID, request IIIF page 1 at thumbnail size (`90,`):

   ```text
   https://portal.yek.gov.tr/iiif/webservice/ShowImage/{candidate_id}/1/full/90,/0/default.jpg
   ```

3. A **placeholder / error response** is exactly **2457 bytes**. A real IIIF page returns significantly more data (typically 8–80 KB for a thumbnail).
4. When you find a candidate whose p1 response is NOT 2457 bytes, confirm identity by checking p1 visually (should match the manuscript's title page) and by checking that the total page count matches what YEK metadata records for that manuscript.
5. This technique confirmed IIIF ID `0000000664425` for Arkeoloji Recaizade Ekrem Bey 00066 (YEK 705856).

### Rendering IIIF images for screenshot

Navigating directly to a IIIF JPEG URL causes the browser to show binary. Inject into an HTML page:

```js
async (page) => {
  const iiifUrl = 'https://portal.yek.gov.tr/iiif/webservice/ShowImage/{id}/{page}/full/1600,/0/default.jpg';
  await page.setContent(`<!DOCTYPE html><html><body style="margin:0;background:#000">
    <img id="img" src="${iiifUrl}" style="max-width:100%;display:block;" crossorigin="anonymous"/>
  </body></html>`);
  await page.waitForFunction(() => {
    const img = document.getElementById('img');
    return img && img.complete && img.naturalWidth > 0;
  }, { timeout: 15000 });
}
```

Then call `browser_take_screenshot` (do NOT use `page.screenshot()` inside `browser_run_code` — that times out).

## Responsible Querying

- Pause 2–3 seconds between consecutive search requests.
- Do not run more than 20 automated queries in a single session without a longer pause.
- Respect institutional access conditions.
