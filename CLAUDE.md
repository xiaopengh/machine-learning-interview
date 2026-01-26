# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This repository contains a comprehensive Chinese machine learning interview Q&A document (`README.md`) and tooling to convert it into Anki flashcards.

## Commands

### Generate Anki Cards
```bash
python3 convert_to_anki.py
```
This parses `README.md`, extracts Q&A pairs from the "解答" (answers) section, and generates:
- `anki_output/anki_basic_cards.txt` - Standard Q&A cards (tab-separated)
- `anki_output/anki_cloze_cards.txt` - Cloze deletion cards (tab-separated)
- `anki_output/anki_images/` - Downloaded images
- `anki_output/README_import.md` - Import instructions

## Architecture

### Content Flow
```
README.md → parse_readme() → qa_pairs → process_card_content() → generate_anki_files()
```

### Key Processing Steps (in order)
1. **Translation injection** (`term_translations.py`): Adds English translations in parentheses after Chinese ML terms (e.g., "损失函数" → "损失函数(Loss Function)")
2. **Image processing** (`convert_images_to_anki()`): Downloads remote images, converts Zhihu equation URLs to LaTeX, removes broken local file paths
3. **LaTeX conversion** (`convert_latex_to_anki()`): Converts `$...$` and `$$...$$` to `<anki-mathjax>` tags (Anki does not render dollar-sign delimiters)
4. **Markdown to HTML** (`markdown_to_html()`): Converts bold, italic, code blocks, lists for Anki's HTML renderer

### Anki-Specific Considerations
- Anki stores notes as HTML, not Markdown
- Math requires `<anki-mathjax>` tags (inline) or `<anki-mathjax block="true">` (display)
- Images must be flat in `collection.media/` (no subdirectories)
- Import format uses tab (`\t`) as field separator

### README.md Structure
The source document has two main sections:
1. **Questions list** (beginning): Table of contents with checkboxes and anchors
2. **Answers section** (starts at `# 解答`): Actual Q&A content to be parsed

Questions are identified by checkbox patterns (`- [ ]` or `- [x]`) with various formats:
- `<span id="X-X">Question</span>`
- `[X-X Question text](#anchor)`
- Plain text after checkbox
