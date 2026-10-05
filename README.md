# Jabez Magomere — personal site

A dependency-free, single-page academic website: semantic HTML, responsive CSS,
no build step and no JavaScript.

## Run locally

```bash
python3 -m http.server 8000
```

Then open <http://localhost:8000>.

Note: `python3 -m http.server` sends no `Cache-Control` or `ETag`, so browsers
cache `style.css` heuristically and a plain reload may not pick up edits. The
stylesheet is therefore linked as `style.css?v=N` — bump `N` in `index.html`
when a CSS change does not appear.

## Layout

| Path | Purpose |
| --- | --- |
| `index.html` | All page content and metadata |
| `style.css` | Layout, type, responsive behaviour, print styles |
| `assets/profile.jpg` | Profile photo and social-preview image |
| `assets/jabez-magomere-cv.pdf` | CV linked from the nav |
| `assets/thumbnails/` | Publication and talk images |
| `assets/logos/` | Inline tech logos and the DeepMind mark |
| `favicon*.{ico,png}` | Favicons, at the root so `/favicon.ico` resolves |
| `scripts/make_thumbnails.py` | Normalises images into site thumbnails |
| `.nojekyll` | Stops GitHub Pages running Jekyll over the files |

## Adding a thumbnail

Marks are square and crop with `object-fit: cover`, so square sources work best.
`scripts/make_thumbnails.py` pads or crops anything else to 800 × 800 WebP:

```bash
python3 scripts/make_thumbnails.py ~/Downloads/paper-figure.png   # pad on white
python3 scripts/make_thumbnails.py --fit photo.jpg                # centre-crop
python3 scripts/make_thumbnails.py --pad-colour "rgb(255,222,89)" slide.png
```

Name the file after the paper, then point the mark at it:

```html
<div class="paper-mark"><img src="assets/thumbnails/paper-name.webp" alt="" width="136" height="136" loading="lazy"></div>
```

Both publication and talk marks render at 136 × 136 px, scaling to 112 px and
76 px at the 850 px and 470 px breakpoints.

Useful modifier classes on a mark:

- `mark-contain` — show the whole image instead of cropping (non-square sources)
- `mark-diagram` — padding plus the accent tint, for vector diagrams
- `mark-grey`, `mark-yellow`, `mark-lavender`, `mark-dark` — background tints

### Animated SVG thumbnails

An animated SVG is embedded with `<img>`, and **Chromium does not propagate
`prefers-reduced-motion` into an SVG loaded that way** — the SVG's own
media-query guard never fires. Pair it with a static fallback instead:

```html
<div class="paper-mark mark-diagram"><picture>
  <source srcset="assets/thumbnails/name.webp" media="(prefers-reduced-motion: reduce)">
  <img src="assets/thumbnails/name.svg" alt="" width="136" height="136" loading="lazy">
</picture></div>
```

The `.webp` in that `srcset` is load-bearing — it is only referenced there, so a
naive "unused files" sweep will suggest deleting it.

## Deploy

Static files, no build. GitHub Pages serves the repository root directly.

1. Push to GitHub.
2. Settings → Pages → Source: *Deploy from a branch*, branch `main`, folder `/ (root)`.
3. Settings → Pages → Custom domain: enter the domain. GitHub writes a `CNAME`
   file and provisions TLS.
4. In Cloudflare DNS, point the domain at GitHub Pages (see below).

Every push to `main` republishes the site; there is no workflow to maintain.

## Before launch

- [ ] Set `og:url` and add `<link rel="canonical">` once the domain is live.
- [ ] Make `og:image` and `twitter:image` **absolute** URLs — relative paths are
      ignored by Twitter/X, LinkedIn and Slack when generating previews.
- [ ] Add the INCLUDE-2.0 paper link (the only publication without one).
