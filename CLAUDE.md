# Khandan Calligrapher Research Project

## Overview

This project finds and confirms manuscripts written by the calligrapher **Sultan Muhammad Khandan** (سلطان محمد خندان, laqab: خندان, "smiling") — a leading nastaʿlīq scribe associated with Herat and the patronage circle of Mir ʿAlī Shīr Navāʾī, active approximately 915–992 AH (1509–1584 CE).

The pipeline searches the YEK portal (Yazma Eserler Kurumu Başkanlığı, portal.yek.gov.tr) for manuscripts attributed to Khandan, then visually confirms each attribution by reading his signature in the manuscript's colophon.

## Key Conventions

- **Memory**: All agents must read `MEMORY.md` before starting work and update it after completing significant tasks. This prevents duplicate work across sessions.
- **Terminology**: Use IJMES transliteration for Arabic and Persian. Use modern Turkish orthography for Ottoman Turkish terms. Always include original Arabic/Persian script where relevant.
- **Output format**: All structured data output as JSON, UTF-8 encoding.
- **File naming**: Search results use `search_{date}_{term}.json`. Colophon screenshots use `{collection}_{shelfmark}_p{page}_{method}.png`.
- **Confidence scoring**: All verdicts must include a confidence score (0.0–1.0) and justification.

## Pipeline

```text
User requests Khandan search
    → khandan-search (query YEK portal via Playwright MCP)
        Search Nüshayla ilgili kişiler, Mühürler ve Kayıtlar, Genel Notlar
        Apply term tiers (Arabic script → colophon kernels → Latin transliterations)
        Filter false positives (Handan as Turkish name, wrong Khandan, Sultan Muhammad Nur)
        Save to catalog/searches/search_{date}_{term}.json
        Update MEMORY.md

    → colophon-verifier (for each genuine result with digital images)
        Check if colophon text already transcribed in Mühürler ve Kayıtlar
        Navigate to YEK detail page; extract IIIF ID via network interception
        Navigate to last 5–10 pages of manuscript (colophon location)
        Acquire IIIF images at ≥1600px width for text reading
        Read Arabic script with vision — identify signature formula + خندان name
        Produce ColophonVerdict JSON
        Save screenshots to corpus/colophon_screenshots/
        Update MEMORY.md
```

## Agent Delegation Rules

- **Always** use `khandan-search` when searching the YEK portal for Khandan manuscripts.
- **Always** use `colophon-verifier` to confirm attribution from digitized images.
- Do not run `colophon-verifier` on manuscripts with `no_images` — record as awaiting visual confirmation.
- If a manuscript's `Mühürler ve Kayıtlar` field already contains a transcription of the colophon with Khandan's name, `colophon-verifier` should still confirm visually where images are available (metadata transcription is supporting evidence, not proof alone).

## Agents

| Agent | Model | Role |
| --- | --- | --- |
| `khandan-search` | Opus | YEK portal search for calligrapher attribution via Playwright MCP |
| `colophon-verifier` | Opus | Visual colophon confirmation via Playwright MCP + Claude vision |

## Skills

| Skill | Used by | Content |
| --- | --- | --- |
| `khandan-playbook` | both agents | Search procedures, term tiers, false positive rules, IIIF navigation |
| `colophon-guide` | colophon-verifier | Colophon identification, Khandan signature formulas, navigation to end of manuscript |
| `output-schemas` | both agents | JSON schemas for search results, colophon verdicts, manuscript records |

## Online Catalog Sweep (Firecrawl)

After exhausting the YEK portal, run a Firecrawl-based sweep of external catalogs to discover manuscripts and enrich existing records. Workflow:

1. **Scrape** target URLs in parallel: `FIRECRAWL_API_KEY=... firecrawl scrape <url> -o .firecrawl/catalogs/<name>.md`
2. **Web search** for English + Persian queries: `firecrawl search "<query>" -o .firecrawl/catalogs/<name>.json`
3. **Analyze** each result against `catalog/world_corpus.json` — identify new manuscripts, colophon transcriptions, provenance, date clarifications
4. **Update corpus** via Python script (write to `.firecrawl/scratchpad/`, execute separately — do not use Bash heredoc for large scripts)
5. **Update** `REPORT.md` tables and `MEMORY.md` session log

Key sources: FIHRIST person pages, baysunghur.org, Chester Beatty catalog PDFs, auction houses (Sotheby's, Christie's, Bonhams, Roseberys), institutional catalogs (Gulbenkian, Freer, BL).

## Data Directories

- `catalog/searches/` — YEK search session JSONs, named `search_{date}_{term}.json`
- `catalog/` — confirmed manuscript records, named `{collection}_{shelfmark}.json`
- `.firecrawl/catalogs/` — scraped external catalog pages (Firecrawl output)
- `.firecrawl/scratchpad/` — reusable Python scripts for corpus updates
- `corpus/colophon_screenshots/` — colophon page screenshots
- `Khandan.md` — research notes on search strategy and calligrapher identity (reference document)

## About the Calligrapher

Sultan Muhammad Khandan (خندان, "smiling") was a student of Sultan ʿAlī Mashhadī, active in the Herat scribal tradition. Known signature formulas in his colophons:

- `العبد سلطان محمد الملقب بخندان`
- `كتبه … خندان`
- `حرره … خندان`
- `فقير … خندان`

Activity range: 915–992 AH (1509–1584 CE). Script: nastaʿlīq (nestaʿlīk). Associated geography: Herat (هرات). Possible confusion: Sultan Muhammad Nūr (سلطان محمد نور) — a distinct contemporary.
