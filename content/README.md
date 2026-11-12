# Page content

Every section of the DURF home page is a Markdown file in this folder. Edit the text here:
`index.html` renders it in the browser with the [DURF design system](https://durf-project.github.io/durf-design-system/)
(`durf-site.js`), so there is no build step. Save, push, and the published page picks it up.

- `sections.json` sets which files appear, and in which order.
- `footer.md` is the footer text.
- HTML comments (`<!-- ... -->`) are notes for editors. They do not appear on the page or on the portal.

| File | Section | Layout |
| --- | --- | --- |
| `00-hero.md` | Title, intro and main buttons | hero |
| `01-figures.md` | Key figures, with their sources | stats |
| `02-statement.md` | One sentence on a coloured band | statement |
| `03-about.md` | About / why DURF | media |
| `04-themes.md` | The six themes, one card each | cards |
| `04b-team.md` | Our team: project lead, theme leads, supporting roles, steering group | cards |
| `05-announcements.md` | Announcements, newest first, collapsed | accordion |
| `06-timeline.md` | Milestones from proposal to project end | timeline |
| `07-documents.md` | Documents and tools, one card each | cards |
| `08-get-involved.md` | Call to action with buttons | band |

## Front matter

Each file starts with a short block between `---` lines:

```
---
layout: cards          # hero | stats | statement | cards | features | timeline | media | band | prose | accordion
id: themes             # anchor, so you can link to #themes (keep the existing ones: other sites link to them)
nav: Themes            # label in the bar under the menu (leave out to hide)
eyebrow: Six themes    # small label above the heading
background: muted      # optional: muted or tint
---
```

The hero also takes `image`, `image2`, `image-alt` and `image2-alt` (two screenshots in a frame
with coloured blocks; without them the round DURF logo is shown).

## Writing conventions

- English, sentence case headings, plain and cooperative ("we", "together"). No em dashes.
- `## Heading` is the section title; the paragraphs after it are the intro.
- A list in which the last items are only a link becomes a row of buttons. The first one is the main button.
- **Key figures** (`01-figures.md`): each item is `- **value** label`. Write `Unknown` when a figure has
  not been measured: it is shown muted with a "Not yet measured" label. Never estimate a figure.
  `{theme-3}` at the start of an item sets its colour. Keep the sources paragraph under the list up to date.
- **Cards** (themes, documents): every `### Heading` starts a card. Straight under it you can add a
  block of detail lines: `theme: 2` (colour and "Theme 2" label), `tags: Draft, Live`, `date:` or `number:`.
  A picture on its own line becomes the card picture; screenshots live in `assets/screens/` (960 x 540 pixels).
- **Announcements** (`05-announcements.md`): every `### Heading` is one collapsed item, newest first,
  with a `date:` line straight under it. The heading is also the link anchor:
  `### DURF Federation Day` opens with https://durf-project.github.io/project-page/#durf-federation-day.
- **Timeline**: each item is `- **date** what happens`; the dates become coloured pills.
- The hero has the Federation Day registration as first button. Remove that line after 18 November 2026.

## Preview locally

The page loads these files with `fetch`, so open it through a small web server rather than as a file:
`python3 -m http.server 8000` in the repository folder, then go to http://localhost:8000.
