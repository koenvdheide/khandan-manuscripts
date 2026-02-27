# Colophon Identification Guide

Reference for locating and reading manuscript colophons in the YEK digital image viewer. Used by the `colophon-verifier` agent.

## What is a Colophon?

A **colophon** (Arabic: خاتمة *khātima* or كولوفون; Turkish: *ketebe kaydı* or *istinsah kaydı*; Persian: *tārikh*) is the scribal subscription at the end of a manuscript. It records:

- The copyist/calligrapher's name (and often their role: كتبه, حرره, خطّه)
- Date of completion (in AH numerals)
- Place of writing (often)
- Dedicatee or patron (sometimes)

For Khandan attribution, the colophon is the **primary evidence** — his name and signature formula appear here.

## Where to Find the Colophon

### Location in the manuscript

- **Always near the end**: typically the last 1–3 pages of text, followed by blank endpapers
- After the final words of the main text, there may be a **taṣliya** (blessing: صلّى الله على محمّد وآله) and/or a **dūʿāʾ** (prayer) before the colophon
- In some manuscripts, the colophon occupies the lower third of the last text page

### In the YEK viewer

1. Open the viewer and read the total page count Y (shown as "X / Y")
2. Navigate to page **Y − 4** as your starting point
3. Work backward from Y toward Y − 9 if needed (blank endpapers at the end are common)
4. The **penultimate text page** (Y − 2 or Y − 1 in most cases) is the most common colophon location

### Short manuscripts (Y ≤ 20)

Examine from page Y/2 onward (second half of the manuscript).

## Visual Identification of the Colophon Page

A colophon page is visually distinctive in Persian/Ottoman manuscripts:

### Triangular text arrangement (most common)

- Lines of text get **progressively shorter** toward the end, creating an inverted-triangle or diamond shape
- This is especially characteristic of nastaʿlīq calligraphy from the Timurid/Safavid/Ottoman period
- The scribal signature typically occupies the last 1–3 short lines at the bottom of this triangle

### Other visual cues

- **Finial or tailpiece**: A small ornamental mark (شمسه, ترنج, or simple flourish) may follow the last word
- **End of text**: The text stops mid-page, with blank space below — unusual in the body of a manuscript
- **Different text density**: The colophon is often written in a slightly smaller hand or more compressed layout than the main text
- **Decorative basmala or taṣliya**: May precede the colophon in a separate line with larger script

### What the colophon does NOT look like

- It is not a headpiece (serlevha/ʿunwān) — those are at the beginning
- It is not a catchword (کلمة الربط) at the bottom of a page — those are single words
- It is not a marginal note — it is in the main text block

## Visual Reference Images

Before reading a target colophon, load 2–3 reference images from `corpus/reference_colophons/` to calibrate your vision. Use the Read tool to view each image file.

### Selection logic

1. **Always load**: `arkeoloji_00153_khandan.png` — the confirmed Khandan colophon (gold standard)
2. **Match by text type**: If a Divan, load W.628 (918 AH) or W.631 (946 AH). If a Khamsa, load W.604 or LoC Nizami. No dedicated Bustan reference exists — use the closest Safavid-era example (W.631 or Freer).
3. **Match by era**: For Timurid-era targets, prefer Walters W.604 (885 AH). For Safavid, prefer Walters W.631 (946 AH) or Freer Haft Awrang (963 AH).
4. **Maximum 3 images** — more wastes context without improving accuracy.

### How to use references

After loading the reference images, note:
- The triangular text arrangement and where the scribe's name falls
- The visual weight and spacing of nastaliq colophon text vs. main text
- How خندان appears in Khandan's own hand (from the gold standard)

Then proceed to read the target colophon with this visual context fresh in memory.

### Limitations

- Reference images show *other scribes'* colophons (except the gold standard). Khandan's hand is distinct.
- References calibrate layout recognition and script reading, not handwriting identification.
- If the target manuscript is a muraqqa (album), references for codex colophons are less relevant — look for caption signatures instead.

## Khandan's Known Signature Formulas

These are the signature formulas attested in authenticated Khandan manuscripts. Listed from most explicit to most abbreviated:

### Full formula (most identifiable)

```text
على يد اضعف عباد الله الصمد المنان سلطان محمد الخندان
```

"By the hand of the weakest of God's servants, the Eternal, the Beneficent, Sultan Muhammad al-Khandan"
*(From Arkeoloji 00153 — **visually confirmed** by this project; colophon on f.10a / IIIF page 11)*

```text
كتبه العبد الضعيف سلطان محمد الملقب بخندان
```

"Written by the weak servant Sultan Muhammad surnamed Khandan"

```text
العبد سلطان محمد الملقب بخندان
```

"The servant Sultan Muhammad surnamed Khandan"
*(From Smithsonian / Freer Gallery F1937.22 — explicit and fully attested)*

**Prefix shared across formulas**: `اضعف عباد الله` / `أضعف عبادالله` ("the weakest of God's servants") appears in both the confirmed Arkeoloji formula and in the anonymous colophon of Arkeoloji Recaizade Ekrem Bey 00066. This prefix alone is not diagnostic — it is a common Islamic humility formula — but its presence is consistent with Khandan's style.

### Medium formula (common)

```text
كتبه … خندان
```

"Written by … Khandan" — where `…` may include العبد, الفقير, or the full name

```text
حرره … خندان
```

"Corrected/written by … Khandan"

### Abbreviated formula (use with caution)

```text
فقير خندان
```

or

```text
الفقير … خندان
```

"The poor one Khandan" — humility formula; needs the name `خندان` to follow

```text
خندان
```

The laqab alone, as the sole identifier — treat as `colophon_probable` unless the full name appears elsewhere on the same page.

### Date formula (look for after the signature)

```text
سنه [عدد] / في سنه [عدد]
```

"In the year [number]" — AH date. Expect 915–992 AH (1509–1584 CE).

Numbers in Arabic abjad or Eastern Arabic numerals (٩١٥ = 915, etc.)

## Reading Arabic Script in Screenshots

### Letter-by-letter guidance for خندان

The word خندان consists of 5 letters: خ ن د ا ن

| Letter | Name | Visual in nastaʿlīq |
| --- | --- | --- |
| خ | khe | Angular hook extending below the line; distinctive initial form |
| ن | nun (initial/medial) | Bowl shape, small tooth above; in nastaʿlīq often resembles a small loop |
| د | dal | Short diagonal tooth; does not connect to the following letter |
| ا | alif | Vertical stroke; slightly curved in nastaʿlīq |
| ن | nun (final) | Large curved bowl with a dot below in isolated/final form |

In connected nastaʿlīq, the sequence خند will flow left-to-right as a unit before the non-connecting dal (د) breaks the chain; then ان follows as a separate unit.

**Disambiguation from نور (Nūr)**:

- نور has only 3 letters and is much shorter visually
- Begins with ن (nun), not خ (khe)
- If you read a 3-letter word where you expected 5 letters, you are likely reading نور not خندان

### Reading at low resolution

If the image is at viewer resolution (~1536px total viewport):

- Zoom in on the colophon area using the viewer's zoom before screenshotting
- Use `browser_evaluate` to get the current zoom level or trigger a zoom gesture
- Individual letter strokes may not be distinguishable — mark as `inconclusive` if you cannot resolve the name

At IIIF 1600px width:

- Letters are typically readable for experienced readers
- The diacritical dot below ن (nun final) should be visible
- The hook of خ (khe) should be distinct

### Common challenges

- **Ink fading**: Colophons are sometimes in lighter ink than the main text (they were often added last)
- **Water damage**: End pages are more exposed to damage
- **Tight spacing**: Small script in the colophon may be harder to read than the main text
- **Waqf stamps**: Ownership stamps may overlay the colophon — try to read through them
- **Multiple scribal additions**: The colophon page may have later hands adding notes

## Navigating to the End of the Manuscript

### Using the page number input

Most YEK viewers have a page number input field showing "X / Y":

1. Click on the current page number (the "X" part)
2. Clear and type the target page number (e.g., Y − 4)
3. Press Enter
4. Verify the viewer has updated to the correct page (check counter)

### Using navigation buttons

If direct page input is not available:

- Click the last-page button (▶| or similar) to jump to the final page
- Click back (◀) repeatedly to step backward through the last few pages

### If the viewer is slow

- Wait 3–5 seconds after each page navigation for images to load before screenshotting
- If a page shows as blank or loading, wait and take a second screenshot

## Confidence Assessment

### When to assign `colophon_confirmed` (confidence 0.80–1.0)

- You can clearly read `خندان` or `سلطان محمد خندان` in the colophon image
- The signature formula (كتبه, حرره, العبد, etc.) is also readable
- IIIF or high-resolution image was used

### When to assign `colophon_probable` (confidence 0.50–0.79)

- You can see a short Arabic word at the expected location of the scribe's name that is consistent with خندان but not fully resolved (e.g., you can read خ at the start and ان at the end, with middle letters unclear)
- Resolution is limiting, but the overall visual pattern matches
- Colophon structure (formula verb + short name) is clearly visible

### When to assign `inconclusive` (confidence 0.20–0.49)

- Images are available but text is too faded, overlaid with stamps, or at too low resolution for any letter-level reading
- The page layout suggests a colophon is present but no text can be extracted
- Only viewer-resolution screenshots are available and zoom is insufficient

### When to assign `colophon_not_found`

- All last 10 pages examined and no page has the visual characteristics of a colophon
- Manuscript may be: (a) acephalous/atelous (incomplete), (b) a fragment, or (c) not structured with a colophon (e.g., some album/murakkaʿ formats)

## Special Cases

### Muraqqa (album) format

Albums (مرقع) do not have a single colophon — individual calligraphic samples may have individual signed captions. In this case:

- Look at the captions beneath each specimen (typically small text below the mounted panel)
- Khandan's signature on an album folio would appear as a caption, not a manuscript colophon
- Navigate through all pages, not just the end

### Dīwān (poetry collection)

Dīwāns often have a colophon at the very end of the main text, before the fihrist (table of contents, if present) or endpapers. The colophon is typically after the last poem (ghazal, rubāʿī, or qaṣīda).

### Qurʾān

Quranic manuscripts attributed to Khandan would be exceptional (his known works are primarily literary). If found, the colophon appears after the final verse (typically Sura 114) and before any duʿāʾ section.
