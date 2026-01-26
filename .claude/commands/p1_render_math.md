## Problem Description

Questions and answers were authored under the assumption that Anki supports **Markdown-style LaTeX math delimiters** (`$…$` and `$$…$$`). As a result, many cards contain mathematical expressions written using these delimiters.

However, when these cards are rendered in Anki, the LaTeX inside `$…$` or `$$…$$` is **not rendered** and instead appears as plain text. In contrast, math wrapped using Anki’s `<anki-mathjax>` tag renders correctly.

This leads to:

* broken or unreadable math on cards,
* inconsistent rendering behavior,
* confusion because the same content works in typical Markdown/MathJax environments but fails in Anki.

---

## Explanation

### 1. Anki does not natively support Markdown

Anki note fields are stored and rendered as **HTML**, not Markdown.
Markdown syntax (including `$…$` and `$$…$$`) is **not parsed** unless an external Markdown-rendering add-on is involved—and even then, the rendering order is not guaranteed.

Therefore, writing content in “Markdown format” does not imply it will be interpreted as such by Anki.

---

### 2. MathJax is not automatically triggered by `$…$` / `$$…$$`

Unlike platforms such as Jupyter Notebook, GitHub, or many Markdown renderers, Anki does **not** scan field content for TeX delimiters and then invoke MathJax.

As a result:

* `$…$` and `$$…$$` remain plain text
* MathJax is never invoked
* no LaTeX typesetting occurs

---

### 3. Anki uses an explicit MathJax trigger: `<anki-mathjax>`

In Anki, MathJax rendering is reliably performed **only** when math content is wrapped in Anki’s custom tag:

```html
<anki-mathjax>...</anki-mathjax>
```

For display math:

```html
<anki-mathjax block="true">
\[
...
\]
</anki-mathjax>
```

This tag explicitly signals Anki’s rendering pipeline to pass the content to MathJax after the card HTML is injected.

---

### 4. Why the current content fails

The current questions and answers:

* assume Markdown rendering,
* rely on `$$…$$` to denote display math,
* never invoke `<anki-mathjax>`.

Because of this, Anki treats the LaTeX as ordinary text and does not typeset it.

The issue is therefore **structural**, not syntactic:

* the LaTeX itself is valid,
* but it is never handed to MathJax.

---

### 5. Required correction

Any system generating content for Anki must do **one** of the following:

1. Output math directly using `<anki-mathjax>` tags
2. Convert `$…$` / `$$…$$` into `<anki-mathjax>` blocks at import or render time
3. Use Anki’s native LaTeX mechanism instead of Markdown-style delimiters

Without one of these steps, Markdown-style math will not render in Anki.

## Discussion

You may suggest your opinion on this subject while explaining why you choose the initial implementation and why does your first math rendering setup makes sense in your view.
