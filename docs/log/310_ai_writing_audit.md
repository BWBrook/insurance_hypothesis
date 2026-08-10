# 310 AI-writing audit pass

Date: 2026-06-29

## What was attempted

- Applied the `audit-ai-writing` skill to the main manuscript, main figure captions, supplementary figure captions, submission statements, title page, cover letter, and main/supplementary tables.
- Treated scanner hits as editorial signals, not evidence of authorship. Markdown headings, mathematical lists, figure IDs, and table syntax were mostly false positives and were left intact where they serve the build system.

## What changed

- Tightened the Abstract and Introduction to state the mechanistic problem earlier: correlated environmental forcing only generates insurance if response directions convert shared forcing into compensation rather than synchrony.
- Replaced generic discussion phrasing such as "aligns with", "highlights", "offers one explanation", and "robust across a wide range" with more direct claim-evidence wording.
- Reduced formulaic balance in the Discussion while preserving the central caveats about stress regions, equicorrelated drivers, one-dimensional response slopes, and omitted demographic/spatial/trophic processes.
- Revised the cover letter and significance statement to sound less template-like and more directly authorial.
- Converted bold panel labels in main and supplementary figure captions to plain "Panel A/B/C" wording.

## What was deliberately left alone

- Table structure, equation formatting, manuscript headings, and technical terms of art.
- Citation placement and scientific claims; no new factual claims or references were added.

## Next

- Run manuscript/source checks to confirm citations, makedoc profiles, and DOCX identity sanitising still pass after the prose edits.
