---
name: layout
description: "Generate CSS grid and flexbox layouts, responsive breakpoints, and HTML page scaffolds."
version: "3.2.0"
author: BytesAgain
homepage: https://bytesagain.com
source: https://github.com/bytesagain/ai-skills
tags:
  - layout
  - css
  - grid
  - flexbox
  - responsive
---

# Layout

Generate CSS layouts and page scaffolds for web projects.

## Commands

### grid

Generate a CSS Grid layout from column/row specifications.

```bash
bash scripts/script.sh grid --columns 3 --rows 2 --gap "1rem" --output layout.css
```

### flex

Generate a Flexbox layout with direction, wrap, and alignment options.

```bash
bash scripts/script.sh flex --direction row --wrap --justify space-between --items 4 --output flex.css
```

### responsive

Generate responsive breakpoint media queries for a set of screen sizes.

```bash
bash scripts/script.sh responsive --breakpoints "sm:640,md:768,lg:1024,xl:1280" --output breakpoints.css
```

### scaffold

Generate a full page skeleton HTML file with header, main, sidebar, and footer sections.

```bash
bash scripts/script.sh scaffold --type "holy-grail" --output page.html
```

### spacing

Generate a spacing scale system (margin/padding utility classes).

```bash
bash scripts/script.sh spacing --base 4 --steps 8 --unit px --output spacing.css
```

### analyze

Analyze an existing CSS file and report layout properties, nesting depth, and breakpoint usage.

```bash
bash scripts/script.sh analyze --input styles.css
```

## Output

- `grid`: CSS file with grid container and item rules
- `flex`: CSS file with flex container and child rules
- `responsive`: CSS file with media query blocks
- `scaffold`: HTML file with semantic sections and linked CSS
- `spacing`: CSS file with spacing utility classes
- `analyze`: Report printed to stdout (properties, selectors, breakpoints found)


## Requirements
- bash 4+

## Feedback

https://bytesagain.com/feedback/

---

Powered by BytesAgain | bytesagain.com
