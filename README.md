# project-page

The DURF one-pager: entry point for DURF stakeholders to learn about the project and find links to
each of the six themes.

`durf-project-page.html` is the ready-to-paste HTML for the CMS helptext field at
https://admin.connect.openaire.eu/netherlands/admin-tools/helptexts?pageId=5fc76829f86fcc06d8a8e74c,
published on https://netherlands.openaire.eu/projects.

It uses only [UIkit](https://getuikit.com/docs/introduction) component classes — no `<style>`,
`<script>`, or `<iframe>` — so it passes the CKEditor content filter in the CMS's Source view and
automatically inherits the site's own colours and fonts. Paste the whole file into the "Content"
Source field.

The HTML has a navigation comment banner (`<!-- ==== THEME 4: PRESERVATION ==== -->`) before every
major section, purely to make it easy to find your way around in the CMS's Plain Text/Source view —
these comments are never shown on the live page.

Per-theme progress dashboards link to https://durf-project.github.io/dashboards/ and the planning
link goes to https://durf-project.github.io/durf-gantt/. Deliverable due dates are derived from that
roadmap's project-month numbers (month 1 = June 2026) and are marked "Due (draft)" since they are
computed, not independently confirmed dates. A handful of deliverables that don't have a public
document yet are marked "not yet published" or "link to follow" — see the TODO comment at the top of
the file for the remaining open items.

The footer carries the EU "AI Modified" content label
(https://digital-strategy.ec.europa.eu/en/policies/eu-icons-labelling-ai-generated-content), since
this page was drafted with AI assistance.

Each theme is colour-coded using the official colour from durf-gantt's `themes.csv` (a top bar in the
overview table, a swatch dot and heading underline, and a button accent in that theme's own section).
Since a `<style>` block is not reliable in this CMS, the colours are applied via inline `style=""`
attributes on individual elements rather than CSS classes.

Internal links (agenda/theme anchors, "back to top") are written as `/projects#agenda` rather than a
bare `#agenda`, because netherlands.openaire.eu's client-side router resolves a bare fragment link
relative to the site root, not the current page — clicking it landed on `/#agenda` instead of staying
on `/projects#agenda`. If this page is ever published at a different path, find/replace `/projects#`
with the new path throughout.
