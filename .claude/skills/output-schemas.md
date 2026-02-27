# Output Schemas

JSON schemas for the Khandan research pipeline. All output files use UTF-8 encoding.

## File Naming Conventions

| File type | Pattern | Location |
| --- | --- | --- |
| Search session | `search_{date}_{term_slug}.json` | `catalog/searches/` |
| Confirmed manuscript record | `{collection}_{shelfmark}.json` | `catalog/` |
| Colophon screenshot | `{collection}_{shelfmark}_p{page:03d}_{method}.png` | `corpus/colophon_screenshots/` |

- `{date}`: ISO date YYYY-MM-DD
- `{term_slug}`: lowercase, no spaces or slashes (e.g., `sultan_muhammed_handan`, `khandan_herevi`)
- `{method}`: `iiif` for IIIF downloads, `view` for viewer screenshots
- `{page:03d}`: zero-padded page number (e.g., `p007`, `p187`)

---

## SearchSession

Output of `khandan-search`. One file per search session (may contain multiple term × field combinations).

```json
{
  "search_date": "YYYY-MM-DD",
  "session_id": "search_YYYY-MM-DD_sessionN",
  "searches": [
    {
      "term": "سلطان محمد خندان",
      "field": "nusha_ilgili_kisiler",
      "field_label_turkish": "Nüshayla ilgili kişiler",
      "operator": "İçeren",
      "raw_count": 0,
      "genuine_count": 0,
      "false_positive_count": 0,
      "results": []
    }
  ],
  "total_genuine": 0,
  "total_false_positives": 0,
  "new_false_positive_patterns": [],
  "notes": ""
}
```

---

## SearchResult

One entry in `searches[n].results[]`. Represents a single manuscript found in a search.

```json
{
  "yek_id": 0,
  "yek_url": "https://portal.yek.gov.tr/works/detail/{yek_id}",
  "shelfmark": "",
  "collection": "",
  "collection_city": "",
  "title": "",
  "title_arabic": "",
  "author": "",
  "date_ah": "",
  "date_ce": "",
  "script_type": "",
  "language": "",
  "has_digital_images": true,
  "total_pages": 0,
  "nusha_ilgili_kisiler_text": "",
  "muhurler_ve_kayitlar_text": "",
  "genel_notlar_excerpt": "",
  "colophon_in_metadata": false,
  "colophon_metadata_text": "",
  "false_positive": false,
  "false_positive_reason": "",
  "disambiguation_needed": false,
  "disambiguation_note": "",
  "flag": "",
  "notes": ""
}
```

**Field notes:**

- `flag`: Optional flag for issues requiring follow-up. Values: `date_mismatch`, `script_mismatch`, `disambiguation_needed`, `check_role`.
- `colophon_in_metadata`: `true` if `Mühürler ve Kayıtlar` contains a transcription of Khandan's colophon signature.
- `colophon_metadata_text`: The exact transcribed text from the field.
- `false_positive_reason`: Required when `false_positive: true`.

---

## ColophonVerdict

Output of `colophon-verifier`. One object per manuscript examined.

```json
{
  "yek_id": 0,
  "shelfmark": "",
  "collection": "",
  "verdict": "colophon_confirmed",
  "confidence": 0.0,
  "confidence_breakdown": {
    "resolution_quality": 0.0,
    "colophon_coverage": 0.0,
    "text_legibility": 0.0,
    "limiting_factor": "resolution | coverage | damage | inherent_uncertainty"
  },
  "colophon_text_read": "",
  "signature_formula_found": "",
  "name_in_colophon": "",
  "date_in_colophon": "",
  "date_ah_read": "",
  "date_ce_computed": "",
  "place_in_colophon": "",
  "internal_iiif_id": "",
  "total_pages": 0,
  "pages_examined": [],
  "screenshots_saved": [],
  "colophon_page_number": 0,
  "colophon_in_metadata": false,
  "colophon_metadata_text": "",
  "different_scribe_name": "",
  "verification_date": "YYYY-MM-DD",
  "notes": ""
}
```

**Verdict values:**

- `colophon_confirmed` — name clearly legible in image
- `colophon_probable` — consistent fragments visible, resolution limits certainty
- `colophon_not_found` — examined last pages, no colophon structure found
- `different_scribe` — colophon legible, names a different person (see `different_scribe_name`)
- `colophon_in_metadata` — transcription in YEK metadata confirmed Khandan; images not examined or unavailable
- `no_images` — no digitized images in YEK
- `inconclusive` — images available but unreadable (damage, low resolution)

**Confidence breakdown:**

- `resolution_quality`: 1.0 = IIIF at 1600px+; 0.5 = viewer screenshot; 0.3 = low-zoom viewer
- `colophon_coverage`: fraction of likely colophon pages examined (e.g., 0.5 = 5 of target 10 pages)
- `text_legibility`: 1.0 = every letter clear; 0.5 = most words readable; 0.2 = fragments only
- `limiting_factor`: whichever of the three is lowest

---

## ManuscriptRecord

Final confirmed record for a manuscript with a `colophon_confirmed` or `colophon_probable` verdict. Saved to `catalog/{collection}_{shelfmark}.json`.

```json
{
  "record_id": "{collection}_{shelfmark}",
  "yek_id": 0,
  "yek_url": "https://portal.yek.gov.tr/works/detail/{yek_id}",
  "collection": {
    "institution": "",
    "city": "",
    "country": "Turkey",
    "shelfmark": ""
  },
  "manuscript": {
    "title": "",
    "title_arabic": "",
    "author": "",
    "author_arabic": "",
    "date_ah": "",
    "date_ce": "",
    "script_type": "nastaʿlīq",
    "language": "",
    "folio_count": 0,
    "dimensions_mm": ""
  },
  "attribution": {
    "calligrapher": "Sultan Muhammad Khandan",
    "calligrapher_arabic": "سلطان محمد خندان",
    "calligrapher_laqab": "خندان",
    "evidence_type": "colophon | metadata | catalogue",
    "colophon_verdict": {},
    "nusha_ilgili_kisiler_text": "",
    "muhurler_ve_kayitlar_text": ""
  },
  "search_metadata": {
    "found_via_term": "",
    "found_via_field": "",
    "search_date": "",
    "search_session_file": ""
  },
  "notes": ""
}
```

**`evidence_type` values:**

- `colophon`: Confirmed from colophon image by `colophon-verifier`
- `metadata`: Colophon transcription in YEK Mühürler ve Kayıtlar (visual confirmation not performed or images unavailable)
- `catalogue`: Listed in Nüshayla ilgili kişiler as hattat/müstensih by YEK cataloguer (colophon not found or not examined)

---

## WorldCorpusEntry

One entry in `catalog/world_corpus.json`. Covers all known Khandan manuscripts regardless of source — YEK pipeline results, auction catalogs, museum databases, and scholarly bibliography. This is the authoritative record for the end report.

```json
{
  "record_id": "string",
  "text": {
    "title": "string",
    "title_arabic": "string",
    "author": "string",
    "author_arabic": "string",
    "genre": "string"
  },
  "manuscript": {
    "date_ah": "string",
    "date_ce": "string",
    "date_notes": "string",
    "script_type": "string",
    "language": "string",
    "folio_count": null,
    "dimensions_mm": "string",
    "place_of_copying": "string"
  },
  "holding": {
    "institution": "string",
    "city": "string",
    "country": "string",
    "shelfmark": "string",
    "current_holder_confirmed": true,
    "external_url": "string"
  },
  "attribution": {
    "confidence_level": "confirmed | attributed | catalogued | unverified",
    "source_type": "yek_colophon_verified | yek_cataloguer | auction_catalog | museum_catalog | bibliography",
    "source_citation": "string",
    "colophon_text": "string",
    "signature_formula": "string",
    "our_verification": "string"
  },
  "yek_data": null,
  "status": "complete | pending_verification | awaiting_access | insufficient_data",
  "further_action": "string",
  "notes": "string"
}
```

**`confidence_level` values:**

- `confirmed` — colophon visually verified by this project (colophon-verifier agent)
- `attributed` — signed colophon documented in a credible primary published source (auction catalog with lot description, museum object record)
- `catalogued` — listed in a published scholarly catalog as Khandan copy (Bayani, Karatay, FIHRIST) without our independent colophon verification
- `unverified` — mentioned in secondary literature without a clear primary source citation; identity of text or current location uncertain

**`source_type` values:**

- `yek_colophon_verified` — confirmed through YEK portal + colophon-verifier agent
- `yek_cataloguer` — listed in YEK Nüshayla ilgili kişiler as hattat/müstensih
- `auction_catalog` — cited in Sotheby's, Christie's, Bonhams, or similar sale catalog
- `museum_catalog` — cited in institution's own published or online catalog record
- `bibliography` — cited in Bayani, Karatay, or other scholarly monograph

**`yek_data`:** Present only for records found via the YEK pipeline:

```json
{
  "yek_id": 0,
  "yek_url": "https://portal.yek.gov.tr/works/detail/{yek_id}",
  "colophon_verdict": "string",
  "confidence": 0.0,
  "iiif_id": "string",
  "verdict_file": "string"
}
```

**`status` values:**

- `complete` — fully processed; no further action needed
- `pending_verification` — colophon-verifier has not yet examined; images available
- `awaiting_access` — manuscript exists but images unavailable or institution not yet searched
- `insufficient_data` — record too sparse (e.g., auction comparandum with no known current location)

---

## CorpusIndex

Lightweight index of all manuscripts found and their current pipeline status. Maintained at `catalog/corpus_index.json`.

```json
{
  "last_updated": "YYYY-MM-DD",
  "total_manuscripts": 0,
  "manuscripts": [
    {
      "record_id": "",
      "yek_id": 0,
      "shelfmark": "",
      "collection": "",
      "title": "",
      "date_ah": "",
      "script_type": "",
      "has_digital_images": true,
      "colophon_verdict": "",
      "confidence": 0.0,
      "pipeline_stage": "search_found | colophon_verification | confirmed | awaiting_images",
      "search_date": ""
    }
  ]
}
```
