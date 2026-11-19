# Federation Day illustration

`assets/img/federation-day-2026.jpg`: the group photo of the first DURF Federation Day
(18 November 2026), cut out and placed in front of the opening slide of the presentation.

1. `tiles.py <model> 520 260` runs a background-removal model (rembg: `u2net_human_seg` and
   `isnet-general-use`) on overlapping tiles of the group, because on the whole photo the people
   are too small for the models.
2. `cutout.py` merges both masks, removes the light wall and the chat panel of the screen (it
   shows names), and cuts the people off just above the tables.
3. `hero.mjs` takes the opening slide from the live presentation (without its subtitle and the
   slide controls); `compose.mjs` puts the people in front of it (`compose.html`).

The photo itself (`photo.jpg`) is not in the repository.
