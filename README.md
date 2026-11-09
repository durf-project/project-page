# project-page

Home page of the Dutch Repository Federation (DURF), published with GitHub Pages at
**https://durf-project.github.io/project-page/**, plus a bare HTML version for
https://netherlands.openaire.eu/projects.

```
index.html                         the page, in the DURF design system
content/sections.json              which sections the page shows, and in which order
content/*.md                       the text of each section: edit these
assets/                            logo, favicon and the vendored markdown renderer (marked)
portal/durf-project-page.html      bare HTML for the Netherlands Research Portal (generated)
scripts/build-portal.mjs           builds the portal HTML from content/*.md
.github/workflows/build-portal.yml rebuilds the portal HTML when content/ changes on main
```

## Editing the text

Edit the Markdown files in [`content/`](content). `index.html` fetches and renders them in
the browser, so there is no build step: save, push, and the published page picks it up.

- `about.md`, `announcements.md`, `themes.md` and `documents.md` are the four sections.
- In every file the `#` heading is the section title. In `announcements.md` each
  announcement is a `##` heading with its date, newest first.
- In `themes.md` keep the number and the full stop at the start of each `##` heading
  (`## 3. Full Text Capture`): the page uses the number for the colour dot.
- To add a section, create `content/<name>.md` and add `"<name>"` to `content/sections.json`.
- HTML comments (`<!-- ... -->`) are notes for editors. They do not appear on the portal page.

## The Netherlands Research Portal version

[`portal/durf-project-page.html`](portal/durf-project-page.html) is a bare HTML fragment: no
`<html>`, `<head>`, CSS or scripts, only headings, paragraphs, lists and absolute links, so it
takes on the style of the portal. Copy its content into https://netherlands.openaire.eu/projects.
The portal page has its own `<h1>`, so the section titles are `<h2>` and announcement and
theme titles are `<h3>`.

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
