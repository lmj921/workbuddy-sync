---
name: pptx-executive-translation-beautify
description: Use this skill when a user provides one or more PPTX files and asks to translate, beautify, polish, redesign, or prepare them for an executive meeting or HR/business review. It guides content extraction, translation cleanup, executive-story restructuring, non-destructive output generation, and QA for PPTX deliverables.
description_zh: PPT高管汇报美化翻译
description_en: PPT Executive Translation Polish
disable: false
agent_created: true
---

# pptx-executive-translation-beautify

## When to use

Use this skill when the user provides `.pptx` files and asks for any combination of:
- translation between Chinese and English for an executive audience;
- layout beautification, visual polish, or redesign;
- preparation for HRVP / APAC / leadership / business review meetings;
- merging several rough PPTs into one executive-ready storyline.

If the user explicitly wants to keep the decks separate, output separate decks. If the user mentions an executive meeting or reporting scenario and gives multiple source decks, default to creating an integrated presentation while preserving all meaningful source content.

## Steps

1. Load the built-in PPTX workflow first for file reading/editing guidance.
2. Work non-destructively: never overwrite source files from Downloads/Desktop/Documents. Create outputs in the workspace and deliver those files.
3. Extract source content:
   - Run `python -m markitdown input.pptx > source_text.md` when available.
   - Use `python-pptx` to inspect slide count, text boxes, image count and slide dimensions.
   - Extract `ppt/media/*` from each PPTX if source photos/screenshots should be reused.
4. Decide the executive storyline:
   - Convert raw Chinese bullets into concise English business language.
   - Preserve proper nouns and program names; transliterate ambiguous Chinese names and keep the original meaning in the subtitle if needed.
   - Avoid inventing metrics. Use only metrics found in the source; synthesize qualitative implications separately as “signal”, “outcome”, or “executive message”.
5. Design the deck:
   - Use a clear executive palette, usually dark navy + teal + one warm accent for HR/talent themes.
   - Prefer 16:9, large titles, KPI cards, 3-column portfolio views, process flows, and evidence/photo blocks.
   - Every slide should have at least one visual element: photo, screenshot, icon, KPI, process, or card.
6. Generate the output:
   - For heavy redesign, create a new PPTX with `python-pptx` or `pptxgenjs` instead of trying to mutate crowded source layouts.
   - Reuse source photos/screenshots after cropping/letterboxing so the result looks intentional.
   - Name output files clearly, e.g. `AP_Meeting_Talent_Development_Performance_Update_EN.pptx`.
7. QA:
   - Re-run `markitdown` on the output and check that all source concepts are represented.
   - Search for placeholders: `xxxx|lorem|ipsum|placeholder|this.*(page|slide).*layout`.
   - Check slide count and shape boundaries using `python-pptx`.
   - Render at least a QuickLook thumbnail or PDF/images when available and visually inspect for overlap, clipping, low contrast, cramped spacing, or inconsistent alignment.
8. Deliver:
   - Use the result-view presentation tool for the primary PPTX.
   - Attach the final PPTX, and optionally a preview image or translation/source mapping if useful.

## Pitfalls

- Do not overwrite source PPTX files in personal folders.
- Do not fabricate performance numbers to make the deck look stronger.
- For Chinese program names, do not over-translate brand/program terms. Keep a stable English name, e.g. “Beilei Partner Coaching Program – Cohort 3”.
- Executive decks should not be a literal line-by-line translation; translate into concise business language while preserving meaning.
- Avoid text-only slides and repeated bullet layouts.
- Fonts like Aptos may render unexpectedly on some macOS setups; Arial is safer for broad compatibility.
- KPI labels can overlap when generated programmatically; always preview the first slide and adjust text boxes if needed.

## Verification

Before final response, confirm:
- source files are unchanged;
- output PPTX opens and has the expected slide count;
- final text extraction has no placeholder strings;
- no shape boundary issues are detected;
- at least one visual preview pass was performed and obvious layout issues were fixed.
