#!/usr/bin/env python3
"""
Convert Machine Learning Interview Q&A (README.md) to Anki flashcard format.

Output files:
- anki_output/anki_basic_cards.txt - Standard Q&A format
- anki_output/anki_cloze_cards.txt - Cloze deletion format
- anki_output/anki_images/ - Downloaded images

Import instructions:
- Basic cards: Import as "Basic" note type with tab separator
- Cloze cards: Import as "Cloze" note type with tab separator
"""

import os
import re
import hashlib
import urllib.request
import ssl
from pathlib import Path
from term_translations import add_translations, get_category_tag, TERM_TRANSLATIONS

# Configuration
README_PATH = "README.md"
OUTPUT_DIR = "anki_output"
IMAGES_DIR = os.path.join(OUTPUT_DIR, "anki_images")
BASIC_CARDS_FILE = os.path.join(OUTPUT_DIR, "anki_basic_cards.txt")
CLOZE_CARDS_FILE = os.path.join(OUTPUT_DIR, "anki_cloze_cards.txt")

# SSL context for downloading images
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE


def setup_directories():
    """Create output directories."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(IMAGES_DIR, exist_ok=True)


def fix_url(url):
    """Fix malformed URLs."""
    # Fix double slashes after protocol (https:////example.com -> https://example.com)
    url = re.sub(r'^(https?:)//+', r'\1//', url)
    return url


def decode_zhihu_equation(url):
    """Extract LaTeX from Zhihu equation URL and convert to Anki MathJax."""
    match = re.search(r'zhihu\.com/equation\?tex=([^&\s]+)', url)
    if match:
        import urllib.parse
        latex = urllib.parse.unquote(match.group(1))
        # Determine if it's display or inline math based on content
        if any(cmd in latex for cmd in ['\\begin{', '\\\\', '\\frac', '\\sum', '\\int']):
            return f'<anki-mathjax block="true">{latex}</anki-mathjax>'
        return f'<anki-mathjax>{latex}</anki-mathjax>'
    return None


def is_local_path(url):
    """Check if URL is actually a local file path."""
    # Windows paths like C:\Users\... or relative paths
    return bool(re.match(r'^[A-Za-z]:\\', url) or
                url.startswith('./') or
                url.startswith('../') or
                (not url.startswith('http') and '\\' in url))


def download_image(url, question_id):
    """Download image and return local filename."""
    # Fix malformed URLs
    url = fix_url(url)

    try:
        # Generate filename from URL hash
        url_hash = hashlib.md5(url.encode()).hexdigest()[:8]
        ext = os.path.splitext(url.split("?")[0])[1] or ".png"
        if ext not in [".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"]:
            ext = ".png"
        filename = f"{question_id}_{url_hash}{ext}"
        filepath = os.path.join(IMAGES_DIR, filename)

        # Skip if already downloaded
        if os.path.exists(filepath):
            return filename

        # Download
        print(f"  Downloading: {url[:70]}...")
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10, context=ssl_context) as response:
            with open(filepath, "wb") as f:
                f.write(response.read())
        return filename
    except Exception as e:
        print(f"  Failed to download {url}: {e}")
        return None


def convert_images_to_anki(text, question_id):
    """Convert markdown/HTML images to Anki format and download them."""
    # Pattern for Zhihu-style nested bracket images: ![[公式]](url)
    zhihu_pattern = r"!\[\[([^\]]*)\]\]\(([^)]+)\)"
    # Pattern for markdown images: ![alt](url)
    md_pattern = r"!\[([^\]]*)\]\(([^)]+)\)"
    # Pattern for HTML images: <img src="url">
    html_pattern = r'<img[^>]*src=["\']([^"\']+)["\'][^>]*>'

    def replace_zhihu_image(match):
        """Handle Zhihu-style ![[公式]](url) format."""
        url = match.group(2)
        if 'zhihu.com/equation' in url:
            latex = decode_zhihu_equation(url)
            if latex:
                return latex
        # Fall through to regular image handling
        if url.startswith("http"):
            filename = download_image(url, question_id)
            if filename:
                return f'<img src="{filename}">'
            return "[Image unavailable]"
        return match.group(0)

    # Process Zhihu-style images first (more specific pattern)
    text = re.sub(zhihu_pattern, replace_zhihu_image, text)

    def replace_md_image(match):
        alt = match.group(1)
        url = match.group(2)

        # Skip local file paths
        if is_local_path(url):
            print(f"  Skipping local path: {url[:50]}...")
            return ""  # Remove broken local image reference

        # Convert Zhihu equation URLs to LaTeX
        if 'zhihu.com/equation' in url:
            latex = decode_zhihu_equation(url)
            if latex:
                return latex

        if url.startswith("http"):
            filename = download_image(url, question_id)
            if filename:
                return f'<img src="{filename}">'
            # Failed to download - remove the broken reference
            return f"[Image unavailable: {alt or 'image'}]"
        return match.group(0)

    def replace_html_image(match):
        url = match.group(1)

        # Skip local file paths
        if is_local_path(url):
            print(f"  Skipping local path: {url[:50]}...")
            return ""

        # Convert Zhihu equation URLs to LaTeX
        if 'zhihu.com/equation' in url:
            latex = decode_zhihu_equation(url)
            if latex:
                return latex

        if url.startswith("http"):
            filename = download_image(url, question_id)
            if filename:
                return f'<img src="{filename}">'
            return "[Image unavailable]"
        return match.group(0)

    text = re.sub(md_pattern, replace_md_image, text)
    text = re.sub(html_pattern, replace_html_image, text)
    return text


def convert_latex_to_anki(text):
    """Convert LaTeX math to Anki-compatible MathJax format.

    Anki does not automatically detect $...$ or $$...$$ delimiters.
    Math must be wrapped in <anki-mathjax> tags for MathJax to render.
    """
    # Convert display math $$...$$ to <anki-mathjax block="true">
    # Use DOTALL to handle multi-line formulas
    text = re.sub(
        r'\$\$(.+?)\$\$',
        r'<anki-mathjax block="true">\1</anki-mathjax>',
        text,
        flags=re.DOTALL
    )
    # Convert inline math $...$ to <anki-mathjax>
    # Negative lookbehind/lookahead to avoid matching already-converted $$ or escaped \$
    text = re.sub(
        r'(?<!\$)(?<!\\)\$(?!\$)(.+?)(?<!\\)\$(?!\$)',
        r'<anki-mathjax>\1</anki-mathjax>',
        text
    )
    return text


def markdown_to_html(text):
    """Convert basic markdown to HTML for Anki."""
    # Bold
    text = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"__([^_]+)__", r"<b>\1</b>", text)

    # Italic
    text = re.sub(r"\*([^*]+)\*", r"<i>\1</i>", text)
    text = re.sub(r"_([^_]+)_", r"<i>\1</i>", text)

    # Code blocks
    text = re.sub(r"```[^\n]*\n(.*?)```", r"<pre>\1</pre>", text, flags=re.DOTALL)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)

    # Line breaks
    text = text.replace("\n\n", "<br><br>")
    text = text.replace("\n", "<br>")

    # Lists
    text = re.sub(r"<br>(\d+)\.\s+", r"<br>\1. ", text)
    text = re.sub(r"<br>[-*]\s+", r"<br>• ", text)

    return text


def extract_definition_cloze(text, term):
    """Create cloze deletion for definitions."""
    # Pattern: term是xxx的xxx
    pattern = rf"({re.escape(term)})[是为指]([^。；，]+)"
    match = re.search(pattern, text)
    if match:
        definition = match.group(2)
        return text.replace(definition, f"{{{{c1::{definition}}}}}", 1)
    return None


def create_cloze_cards(question, answer, question_id, tags):
    """Create cloze deletion cards from Q&A content."""
    cloze_cards = []

    # Clean answer for processing
    clean_answer = answer

    # Strategy 1: Definitions (term是xxx)
    for term in TERM_TRANSLATIONS.keys():
        if term in clean_answer:
            cloze = extract_definition_cloze(clean_answer, term)
            if cloze and "{{c1::" in cloze:
                card_text = f"{question}<br><br>{markdown_to_html(cloze)}"
                cloze_cards.append((card_text, tags))
                break  # One cloze per Q&A for definitions

    # Strategy 2: Numbered lists (convert each item to cloze)
    numbered_items = re.findall(r"(\d+)[.、）]\s*([^：:]+)[：:]([^\n]+)", clean_answer)
    if len(numbered_items) >= 2:
        cloze_text = clean_answer
        for i, (num, item_title, item_content) in enumerate(numbered_items[:5], 1):
            # Cloze the item title or key content
            if len(item_title.strip()) > 2:
                cloze_text = cloze_text.replace(
                    item_title, f"{{{{c{i}::{item_title}}}}}", 1
                )
        if "{{c1::" in cloze_text:
            card_text = f"{question}<br><br>{markdown_to_html(cloze_text)}"
            cloze_cards.append((card_text, tags))

    # Strategy 3: Comparisons (A和B的区别/异同)
    if "区别" in question or "异同" in question or "不同" in question:
        # Find comparison items
        comp_pattern = r"([^：:，。]+)使用([^，。；]+)"
        comparisons = re.findall(comp_pattern, clean_answer)
        if len(comparisons) >= 2:
            cloze_text = clean_answer
            for i, (model, feature) in enumerate(comparisons[:4], 1):
                cloze_text = cloze_text.replace(
                    feature, f"{{{{c{i}::{feature}}}}}", 1
                )
            if "{{c1::" in cloze_text:
                card_text = f"{question}<br><br>{markdown_to_html(cloze_text)}"
                cloze_cards.append((card_text, tags))

    # Strategy 4: Key formulas (simple cloze on formula components)
    formula_pattern = r"\$\$([^$]+)\$\$"
    formulas = re.findall(formula_pattern, clean_answer)
    if formulas:
        for formula in formulas[:2]:  # Limit to first 2 formulas
            # Create a cloze card with the formula
            cloze_formula = f"{{{{c1::$${formula}$$}}}}"
            card_text = f"{question}<br><br>公式：{cloze_formula}"
            cloze_cards.append((card_text, tags + " formula"))
            break  # One formula cloze per Q&A

    # Strategy 5: Advantages/Disadvantages lists
    if "优点" in clean_answer or "缺点" in clean_answer or "优缺点" in question:
        # Find bullet points after 优点/缺点
        adv_pattern = r"(优点|缺点)[：:]\s*([^\n]+)"
        advantages = re.findall(adv_pattern, clean_answer)
        if advantages:
            cloze_text = clean_answer
            for i, (adv_type, content) in enumerate(advantages[:4], 1):
                cloze_text = cloze_text.replace(
                    content, f"{{{{c{i}::{content}}}}}", 1
                )
            if "{{c1::" in cloze_text:
                card_text = f"{question}<br><br>{markdown_to_html(cloze_text)}"
                cloze_cards.append((card_text, tags))

    return cloze_cards


def parse_readme():
    """Parse README.md and extract Q&A pairs."""
    with open(README_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # Find the answer section (starts with "# 解答")
    answer_section_match = re.search(r"#\s*解答", content)
    if not answer_section_match:
        print("Could not find '# 解答' section")
        return []

    answer_section = content[answer_section_match.start() :]

    qa_pairs = []
    current_category = "ML"
    current_subcategory = ""

    # Split into lines for processing
    lines = answer_section.split("\n")

    i = 0
    while i < len(lines):
        line = lines[i]

        # Track category headers
        if line.startswith("## "):
            header = line.strip("# ").strip()
            if "机器学习" in header:
                current_category = "ML"
            elif "深度学习" in header:
                current_category = "DL"
            elif "数学" in header:
                current_category = "Math"
            elif "基础工具" in header:
                current_category = "Tools"
            elif "推荐系统" in header:
                current_category = "RecSys"
            # Also check for numbered sections
            if "基本概念" in header:
                current_subcategory = "BasicConcepts"
            elif "特征工程" in header:
                current_subcategory = "FeatureEngineering"
            elif "概率论" in header or "统计" in header:
                current_subcategory = "Probability"
            elif "最优化" in header:
                current_subcategory = "Optimization"

        elif line.startswith("### ") or line.startswith("#### "):
            header = line.strip("# ").strip("*").strip()
            # Map subcategories
            if "特征工程" in header:
                current_subcategory = "FeatureEngineering"
            elif "KNN" in header:
                current_subcategory = "KNN"
            elif "支持向量机" in header or "SVM" in header:
                current_subcategory = "SVM"
            elif "朴素贝叶斯" in header:
                current_subcategory = "NaiveBayes"
            elif "线性回归" in header:
                current_subcategory = "LinearRegression"
            elif "逻辑回归" in header:
                current_subcategory = "LogisticRegression"
            elif "FM" in header:
                current_subcategory = "FM"
            elif "决策树" in header:
                current_subcategory = "DecisionTree"
            elif "随机森林" in header or "RF" in header:
                current_subcategory = "RandomForest"
            elif "GBDT" in header:
                current_subcategory = "GBDT"
            elif "k-means" in header.lower() or "kmeans" in header.lower():
                current_subcategory = "KMeans"
            elif "PCA" in header or "降维" in header:
                current_subcategory = "PCA"
            elif "DNN" in header or "神经网络" in header:
                current_subcategory = "DNN"
            elif "CNN" in header or "卷积" in header:
                current_subcategory = "CNN"
            elif "RNN" in header or "循环" in header or "LSTM" in header:
                current_subcategory = "RNN"
            elif "Spark" in header:
                current_subcategory = "Spark"
            elif "Xgboost" in header or "XGBoost" in header:
                current_subcategory = "XGBoost"
            elif "Tensorflow" in header or "TensorFlow" in header:
                current_subcategory = "TensorFlow"

        # Check if this is a question line (starts with - [ ] or - [x])
        if not re.match(r"^\s*-\s*\[[x\s]\]", line, re.IGNORECASE):
            i += 1
            continue

        # Extract question from various formats
        question_id = None
        question_text = None

        # Pattern 1: - [ ] <span id="X-X">Question</span>
        span_match = re.match(
            r'^\s*-\s*\[[x\s]\]\s*<span[^>]*id=["\']?([\w-]+)["\']?[^>]*>(.+?)</span>',
            line,
            re.IGNORECASE,
        )
        if span_match:
            question_id = span_match.group(1).strip()
            question_text = span_match.group(2).strip()

        # Pattern 2: - [ ] [X-X Question text](#anchor) or - [ ] [X-X Question text](anchor)
        if not question_text:
            link_match = re.match(
                r'^\s*-\s*\[[x\s]\]\s*\[(.+?)\]\(#?([\w-]*)\)',
                line,
                re.IGNORECASE,
            )
            if link_match:
                question_text = link_match.group(1).strip()
                anchor = link_match.group(2).strip()
                # Extract ID from question text if present
                id_in_text = re.match(r'(\d+-\d+(?:-\d+)?)\s+(.+)', question_text)
                if id_in_text:
                    question_id = id_in_text.group(1)
                    question_text = id_in_text.group(2)
                elif anchor:
                    question_id = anchor

        # Pattern 3: Plain text after checkbox - [ ] Question text
        if not question_text:
            plain_match = re.match(
                r'^\s*-\s*\[[x\s]\]\s*(.+)',
                line,
                re.IGNORECASE,
            )
            if plain_match:
                question_text = plain_match.group(1).strip()
                # Try to extract ID from beginning
                id_in_text = re.match(r'(\d+-\d+(?:-\d+)?)\s+(.+)', question_text)
                if id_in_text:
                    question_id = id_in_text.group(1)
                    question_text = id_in_text.group(2)

        # Skip if no question extracted
        if not question_text:
            i += 1
            continue

        # Generate ID if not found
        if not question_id:
            question_id = f"q-{len(qa_pairs)+1}"

        # Clean question text
        question_text = re.sub(r'\]\(#?[\w-]*\)$', '', question_text).strip()
        question_text = re.sub(r'^\[', '', question_text).strip()
        question_text = re.sub(r'\]$', '', question_text).strip()

        # Collect answer (everything until next question or header)
        answer_lines = []
        i += 1
        while i < len(lines):
            next_line = lines[i]
            # Stop at next question or major header
            if re.match(r"^\s*-\s*\[[x\s]\]", next_line, re.IGNORECASE):
                break
            if re.match(r"^#{1,4}\s+", next_line):
                break
            answer_lines.append(next_line)
            i += 1

        # Process answer
        answer = "\n".join(answer_lines).strip()

        # Build tags
        tags = f"{current_category}::{current_subcategory}"

        # Mark if no answer content
        has_answer = answer and len(answer) >= 10

        qa_pairs.append(
            {
                "id": question_id,
                "question": question_text,
                "answer": answer if has_answer else "",
                "category": current_category,
                "subcategory": current_subcategory,
                "tags": tags,
                "has_answer": has_answer,
            }
        )

    return qa_pairs


def process_card_content(text, question_id):
    """Process card content: add translations, convert images, format."""
    # Add English translations
    text = add_translations(text)

    # Convert images
    text = convert_images_to_anki(text, question_id)

    # Convert LaTeX
    text = convert_latex_to_anki(text)

    # Convert markdown to HTML
    text = markdown_to_html(text)

    # Escape tabs and newlines for TSV format
    text = text.replace("\t", "    ")

    return text


def generate_anki_files(qa_pairs):
    """Generate Anki-compatible output files."""
    basic_cards = []
    cloze_cards = []

    print(f"Processing {len(qa_pairs)} Q&A pairs...")

    for qa in qa_pairs:
        question_id = qa["id"]
        question = qa["question"]
        answer = qa["answer"]
        tags = qa["tags"]

        print(f"  Processing {question_id}: {question[:40]}...")

        # Process content
        processed_question = process_card_content(question, question_id)
        processed_answer = process_card_content(answer, question_id)

        # Basic card
        basic_cards.append((processed_question, processed_answer, tags))

        # Cloze cards
        cloze_list = create_cloze_cards(
            processed_question, answer, question_id, tags
        )
        cloze_cards.extend(cloze_list)

    # Write basic cards file
    print(f"\nWriting {len(basic_cards)} basic cards to {BASIC_CARDS_FILE}")
    with open(BASIC_CARDS_FILE, "w", encoding="utf-8") as f:
        # Header comment
        f.write("# Machine Learning Interview Q&A - Basic Cards\n")
        f.write("# Format: Question<tab>Answer<tab>Tags\n")
        f.write("# Import as 'Basic' note type in Anki\n\n")

        for question, answer, tags in basic_cards:
            f.write(f"{question}\t{answer}\t{tags}\n")

    # Write cloze cards file
    print(f"Writing {len(cloze_cards)} cloze cards to {CLOZE_CARDS_FILE}")
    with open(CLOZE_CARDS_FILE, "w", encoding="utf-8") as f:
        # Header comment
        f.write("# Machine Learning Interview Q&A - Cloze Cards\n")
        f.write("# Format: Text<tab>Tags\n")
        f.write("# Import as 'Cloze' note type in Anki\n\n")

        for text, tags in cloze_cards:
            f.write(f"{text}\t{tags}\n")

    return len(basic_cards), len(cloze_cards)


def create_import_readme():
    """Create README with import instructions."""
    readme_content = """# Anki Import Instructions

## Files Generated

- `anki_basic_cards.txt` - Standard Q&A flashcards
- `anki_cloze_cards.txt` - Cloze deletion flashcards
- `anki_images/` - Downloaded images for cards

## How to Import

### Step 1: Copy Images to Anki Media Folder

Copy all files from `anki_images/` to your Anki media folder:
- **Windows**: `%APPDATA%\\Anki2\\<profile>\\collection.media`
- **Mac**: `~/Library/Application Support/Anki2/<profile>/collection.media`
- **Linux**: `~/.local/share/Anki2/<profile>/collection.media`

### Step 2: Import Basic Cards

1. Open Anki
2. File → Import
3. Select `anki_basic_cards.txt`
4. Set:
   - Type: Basic
   - Deck: (create new or select existing)
   - Fields separated by: Tab
   - Field 1: Front
   - Field 2: Back
   - Field 3: Tags
5. Click Import

### Step 3: Import Cloze Cards

1. File → Import
2. Select `anki_cloze_cards.txt`
3. Set:
   - Type: Cloze
   - Fields separated by: Tab
   - Field 1: Text
   - Field 2: Tags
4. Click Import

## Tag Structure

Cards are tagged with the format: `Category::Subcategory`

Categories:
- ML (Machine Learning)
- DL (Deep Learning)
- Math (Mathematics)
- Tools (Spark, XGBoost, TensorFlow)
- RecSys (Recommender Systems)

Subcategories include:
- BasicConcepts, FeatureEngineering
- KNN, SVM, NaiveBayes, LinearRegression, LogisticRegression
- FM, DecisionTree, RandomForest, GBDT, KMeans, PCA
- DNN, CNN, RNN
- Spark, XGBoost, TensorFlow
- Probability, Optimization

## Customization

### Adding More Translations

Edit `term_translations.py` to add more Chinese-English term pairs.

### Regenerating Cards

Run `python convert_to_anki.py` to regenerate all cards.

## Notes

- Cards include English translations for key ML terms in parentheses
- LaTeX math is converted to `<anki-mathjax>` tags for native Anki rendering (no extra setup needed)
- Images are downloaded locally for offline use
- Zhihu equation images are automatically converted to LaTeX
- Cloze cards are generated for definitions, lists, and key formulas
"""

    with open(os.path.join(OUTPUT_DIR, "README_import.md"), "w", encoding="utf-8") as f:
        f.write(readme_content)


def main():
    """Main entry point."""
    print("=" * 60)
    print("ML Interview Q&A to Anki Converter")
    print("=" * 60)

    # Setup
    setup_directories()

    # Parse README
    print("\nParsing README.md...")
    qa_pairs = parse_readme()
    print(f"Found {len(qa_pairs)} Q&A pairs")

    if not qa_pairs:
        print("No Q&A pairs found. Check README.md format.")
        return

    # Generate Anki files
    print("\nGenerating Anki cards...")
    basic_count, cloze_count = generate_anki_files(qa_pairs)

    # Create import instructions
    create_import_readme()

    # Summary
    print("\n" + "=" * 60)
    print("Conversion Complete!")
    print("=" * 60)
    print(f"\nOutput directory: {OUTPUT_DIR}/")
    print(f"  - anki_basic_cards.txt: {basic_count} cards")
    print(f"  - anki_cloze_cards.txt: {cloze_count} cards")
    print(f"  - anki_images/: Downloaded images")
    print(f"  - README_import.md: Import instructions")
    print("\nSee README_import.md for Anki import instructions.")


if __name__ == "__main__":
    main()
