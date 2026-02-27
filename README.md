# Sultan Muhammad Khandan — Manuscript Corpus

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC_BY_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

A research corpus tracking manuscripts written by the calligrapher **Sultan Muhammad Khandan** (سلطان محمد خندان), a leading nastaʿlīq scribe of the Timurid–Safavid transition, active 915–972+ AH (1509–1564+ CE) in Herat.

## The calligrapher

Khandan (خندان, "smiling") was a student of Sultan ʿAlī Mashhadī and worked within the patronage circle of Mīr ʿAlī Shīr Navāʾī. His signed colophons use formulas such as:

- `العبد سلطان محمد الملقب بخندان`
- `كتبه الفقير خندان`
- `على يد اضعف عباد الله … سلطان محمد الخندان`

He is distinct from Sultan Muhammad Nūr (سلطان محمد نور), a contemporary scribe in the same milieu.

## Corpus

The corpus currently contains **48 manuscripts and album leaves** across institutions worldwide, ranging from codices (Bustān, Dīwān-i Ḥāfiẓ, Subḥat al-Abrār, Yūsuf va Zulaykha, etc.) to single-folio calligraphic specimens (qiṭʿa). See [`catalog/world_corpus.json`](catalog/world_corpus.json) for the full structured dataset and [`REPORT.md`](REPORT.md) for the annotated research report with chronological tables and bibliography.

### Confidence levels

| Level | Count | Meaning |
|-------|------:|---------|
| Confirmed | 1 | Colophon visually verified by this project |
| Attributed | 12 | Signed colophon documented in a primary source |
| Catalogued | 29 | Listed in scholarly catalogs without independent verification |
| Unverified | 5 | Requires further investigation |
| Bibliographic error | 1 | Resolved as misattribution or duplicate |

## Methodology

1. **YEK portal search** — exhaustive search of Turkey's manuscript portal ([portal.yek.gov.tr](https://portal.yek.gov.tr)) across all relevant fields using Arabic-script, colophon-kernel, and Latin-transliteration search terms
2. **Colophon verification** — visual confirmation of scribe signatures in digitized manuscripts via IIIF image acquisition and Arabic-script reading
3. **Online catalog sweep** — cross-referencing FIHRIST, museum catalogs (Chester Beatty, Gulbenkian, Freer, BL), auction records (Sotheby's, Christie's, Bonhams, Roseberys), and secondary literature (Bayani 1966, baysunghur.org)

## Built with Claude Code

The search and verification pipeline uses [Claude Code](https://claude.ai/code) with two specialized agents:

- **khandan-search** — automated YEK portal search via Playwright MCP
- **colophon-verifier** — visual colophon reading using Claude's vision capabilities with few-shot reference calibration

Agent definitions and skills are in [`.claude/`](.claude/).

## Repository structure

```
catalog/
  world_corpus.json          # 48-entry structured corpus
  corpus_index.json          # Index by collection
  *_verdict.json             # Colophon verification verdicts
references/
  colophons_visual_guide.md  # Links to freely accessible colophon images
REPORT.md                    # Full research report with tables and bibliography
CLAUDE.md                    # Project instructions for Claude Code agents
```

Colophon screenshots (~61 images, ~60 MB) are excluded from the repository. The `corpus/` directory is gitignored.

## License

This work is licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Manuscript images referenced in this project remain under their respective institutional licenses.
