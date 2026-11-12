# project-page

Home page of the Dutch Repository Federation (DURF), published with GitHub Pages at
**https://durf-project.github.io/project-page/**, plus a bare HTML version for
https://netherlands.openaire.eu/projects. The organisation address https://durf-project.github.io/
forwards here (see [durf-project.github.io](https://github.com/durf-project/durf-project.github.io)).

```
index.html                         the page: design system v1.1 site components, no styles of its own
content/sections.json              which sections the page shows, and in which order
content/*.md                       the text of each section, with front matter: edit these
content/README.md                  how to write and edit the sections
assets/screens/                    screenshots used on the cards and in the hero
assets/marked.min.js               Markdown renderer for the portal build script
assets/durf-logo.svg, durf-favicon.png  old copies, kept for sites that link to them (the page uses the design system's)
portal/durf-project-page.html      bare HTML for the Netherlands Research Portal (generated)
scripts/build-portal.mjs           builds the portal HTML from content/*.md
.github/workflows/build-portal.yml rebuilds the portal HTML when content/ changes on main
.github/ISSUE_TEMPLATE/feedback.yml the form behind the feedback button
```

## Editing the text

Edit the Markdown files in [`content/`](content). `index.html` loads the
[DURF design system](https://durf-project.github.io/durf-design-system/) (`durf.css`, `durf-site.css`,
`durf-nav.js`, `durf-site.js`), which fetches and renders them in the browser: save, push, and the
published page picks it up. The page has no colours, fonts or layout code of its own.

Each file starts with front matter that picks the layout (hero, key figures, cards, accordion,
timeline and so on). The conventions per section, such as how to add an announcement, mark a key
figure as unknown or colour a card by theme, are in [`content/README.md`](content/README.md).

## The Netherlands Research Portal version

[`portal/durf-project-page.html`](portal/durf-project-page.html) is a bare HTML fragment: no
`<html>`, `<head>`, CSS or scripts, only headings, paragraphs, lists and absolute links, so it
takes on the style of the portal. Copy its content into https://netherlands.openaire.eu/projects.
The portal page has its own `<h1>`, so the section titles are `<h2>` and announcement, theme and
document titles are `<h3>`. The script strips the front matter and the detail lines under headings
(an announcement keeps its date), leaves out pictures and the hero buttons, shows the key figures as
a simple list and the statement as a quote, and makes all links absolute.

The file is generated from `content/*.md`. When `content/` changes on `main`, the workflow
`build-portal.yml` regenerates it and commits the result. To do it yourself:

```
node scripts/build-portal.mjs           # write portal/durf-project-page.html
node scripts/build-portal.mjs --check   # fail if the file is out of date
```

## Previewing locally

Opening `index.html` directly (`file://`) does not load the Markdown files, because browsers
block that fetch. Run a local server instead: `python3 -m http.server`, then open
`http://localhost:8000`.

## Licence

EUPL v1.2, see [LICENSE](LICENSE).
