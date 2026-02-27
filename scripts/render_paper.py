"""Convert PAPER.md to paper.html with academic print-ready CSS.

Usage: python scripts/render_paper.py
Output: paper.html (open in browser → Print to PDF)
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

import markdown
import re

PAPER_PATH = r"c:\Users\koen_\Documents\Projects\Khandan\PAPER.md"
OUTPUT_PATH = r"c:\Users\koen_\Documents\Projects\Khandan\paper.html"

with open(PAPER_PATH, 'r', encoding='utf-8') as f:
    md_text = f.read()

# Convert footnotes: [^1] style → HTML
# markdown package with footnotes extension handles this
html_body = markdown.markdown(
    md_text,
    extensions=['tables', 'footnotes', 'toc', 'smarty'],
    extension_configs={
        'footnotes': {
            'BACKLINK_TEXT': '↩',
        },
        'toc': {
            'permalink': False,
        },
    },
    output_format='html5'
)

# Wrap Arabic/Persian text in bdi tags for proper RTL rendering
# Match sequences of Arabic Unicode characters (0600-06FF, FB50-FDFF, FE70-FEFF)
arabic_re = re.compile(r'([\u0600-\u06FF\uFB50-\uFDFF\uFE70-\uFEFF][\u0600-\u06FF\uFB50-\uFDFF\uFE70-\uFEFF\s\u0640\u200C\u200D\u060C\u061B\u061F\u066B\u066C\u0660-\u0669]*)')

def wrap_arabic(match):
    text = match.group(1)
    # Don't wrap if already inside a tag
    return f'<bdi dir="rtl" class="arabic">{text}</bdi>'

# Only apply outside of HTML tags
def apply_bdi(html):
    parts = re.split(r'(<[^>]+>)', html)
    result = []
    for part in parts:
        if part.startswith('<'):
            result.append(part)
        else:
            result.append(arabic_re.sub(wrap_arabic, part))
    return ''.join(result)

html_body = apply_bdi(html_body)

# Convert <p><img ...></p>\n<p><em>Figure N. ...</em></p> into <figure>+<figcaption>
def wrap_figures(html):
    pattern = re.compile(
        r'<p>(<img\s[^>]+>)</p>\s*<p><em>(Figure\s+\d+\.\s.*?)</em></p>',
        re.DOTALL
    )
    def figure_replace(m):
        img_tag = m.group(1)
        caption = m.group(2)
        return f'<figure>\n  {img_tag}\n  <figcaption>{caption}</figcaption>\n</figure>'
    return pattern.sub(figure_replace, html)

html_body = wrap_figures(html_body)

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Crimson+Text:ital,wght@0,400;0,600;0,700;1,400;1,600&family=Amiri:ital,wght@0,400;0,700;1,400;1,700&display=swap');

:root {
    --text-color: #1a1a1a;
    --heading-color: #2c1810;
    --link-color: #8b4513;
    --border-color: #ccc;
    --bg-light: #f9f7f4;
    --font-body: 'Crimson Text', 'Georgia', serif;
    --font-arabic: 'Amiri', 'Traditional Arabic', 'Scheherazade', serif;
}

* { box-sizing: border-box; }

html {
    font-size: 11.5pt;
    line-height: 1.65;
}

body {
    font-family: var(--font-body);
    color: var(--text-color);
    max-width: 42em;
    margin: 0 auto;
    padding: 2em 1.5em;
    background: #fff;
}

/* Front matter */
h1 {
    font-size: 1.6em;
    font-weight: 700;
    color: var(--heading-color);
    line-height: 1.25;
    margin-bottom: 0.3em;
    text-align: center;
    border-bottom: none;
}

h1 + p > strong:first-child {
    /* Abstract label */
}

/* Section headings */
h2 {
    font-size: 1.25em;
    font-weight: 700;
    color: var(--heading-color);
    margin-top: 2em;
    margin-bottom: 0.5em;
    border-bottom: 1px solid var(--border-color);
    padding-bottom: 0.2em;
}

h3 {
    font-size: 1.05em;
    font-weight: 600;
    color: var(--heading-color);
    margin-top: 1.5em;
    margin-bottom: 0.4em;
}

p { margin: 0.8em 0; text-align: justify; }

/* Arabic text */
.arabic, bdi[dir="rtl"] {
    font-family: var(--font-arabic);
    font-size: 1.05em;
    direction: rtl;
    unicode-bidi: isolate;
}

/* Blockquotes (for colophon transcriptions) */
blockquote {
    font-family: var(--font-arabic);
    font-size: 1.05em;
    direction: rtl;
    text-align: right;
    margin: 1em 2em;
    padding: 0.8em 1em;
    border-right: 3px solid var(--link-color);
    border-left: none;
    background: var(--bg-light);
    line-height: 2;
}

blockquote + p {
    /* Translation after Arabic blockquote */
}

/* Tables */
table {
    width: 100%;
    border-collapse: collapse;
    margin: 1em 0;
    font-size: 0.9em;
    line-height: 1.4;
}

th {
    background: var(--bg-light);
    font-weight: 600;
    text-align: left;
    padding: 0.4em 0.6em;
    border-bottom: 2px solid var(--heading-color);
}

td {
    padding: 0.35em 0.6em;
    border-bottom: 1px solid #e0e0e0;
    vertical-align: top;
}

tr:hover { background: #faf8f5; }

/* Right-align numeric columns */
td:last-child, th:last-child {
    text-align: right;
}

/* Footnotes */
.footnote {
    font-size: 0.85em;
    line-height: 1.5;
    margin-top: 3em;
    border-top: 1px solid var(--border-color);
    padding-top: 1em;
}

.footnote-ref { font-size: 0.8em; vertical-align: super; }

.footnote ol { padding-left: 1.5em; }
.footnote li { margin-bottom: 0.5em; }
.footnote-backref { text-decoration: none; margin-left: 0.3em; }

/* Horizontal rules */
hr {
    border: none;
    border-top: 1px solid var(--border-color);
    margin: 2em 0;
}

/* Links */
a { color: var(--link-color); text-decoration: none; }
a:hover { text-decoration: underline; }

/* Bold for emphasis in tables */
strong { font-weight: 700; }

/* Figures */
figure {
    margin: 1.5em 0;
    text-align: center;
    page-break-inside: avoid;
}
figure img {
    max-width: 100%;
    height: auto;
    border: 1px solid #e0e0e0;
}
figcaption {
    font-family: var(--font-body);
    font-size: 0.85em;
    margin-top: 0.5em;
    text-align: justify;
    color: #555;
    line-height: 1.4;
    padding: 0 1em;
}

/* Appendix tables: smaller font */
h2:nth-of-type(n+9) ~ table {
    font-size: 0.82em;
}

/* Print styles */
@media print {
    html { font-size: 10pt; }
    body { max-width: none; padding: 0; margin: 0; }

    h1, h2, h3 { page-break-after: avoid; }
    table, blockquote, figure { page-break-inside: avoid; }
    .footnote { page-break-before: avoid; }

    a { color: var(--text-color); }
    a[href^="http"]::after {
        content: none; /* Don't print URLs inline */
    }

    @page {
        size: A4;
        margin: 2cm 2.5cm;
    }

    @page :first {
        margin-top: 4cm;
    }

    /* Landscape for wide appendix tables */
    .appendix-landscape {
        page-break-before: always;
    }
    .appendix-landscape table {
        font-size: 0.75em;
    }
}
"""

html_doc = f"""<!DOCTYPE html>
<html lang="en" dir="ltr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sultan Muhammad Khandan — A Corpus of Manuscripts</title>
    <style>{CSS}</style>
</head>
<body>
{html_body}
</body>
</html>
"""

with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
    f.write(html_doc)

print(f"Written to {OUTPUT_PATH}")
# Count approximate words
words = len(re.findall(r'\b\w+\b', md_text))
print(f"Approximate word count: {words}")
