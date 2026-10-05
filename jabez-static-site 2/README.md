# Jabez Magomere — personal site

A dependency-free, single-page academic website built with semantic HTML and responsive CSS.

## Run locally

From this directory:

```bash
python -m http.server 8000
```

Then open `http://localhost:8000`.

## Main files

- `index.html` — all page content and metadata
- `style.css` — layout, type, responsive behaviour, and print styles
- `assets/profile.jpg` — profile and social-preview image
- `assets/favicon.svg` — browser icon

The previous data and bibliography files are retained as source material, but the published page is intentionally static: research content remains readable by crawlers and when JavaScript is disabled.

## Add publication and talk images

Use square images with a `1:1` aspect ratio. Export them at `800 × 800 px` (at least `600 × 600 px`) as WebP, JPG, or PNG, ideally below 300 KB. Keep important text and graphics away from the edges because the site crops thumbnails with `object-fit: cover`.

Put the files in an `assets/thumbnails/` folder. Then replace a placeholder such as:

```html
<div class="paper-mark" aria-hidden="true"><svg>...</svg><span>2026</span></div>
```

with:

```html
<div class="paper-mark"><img src="assets/thumbnails/paper-name.webp" alt=""></div>
```

Use the same pattern with `talk-mark` for tutorial and talk images. The site displays publication thumbnails at 136 × 136 px and talk thumbnails at 92 × 92 px on desktop, then scales them down responsively.

## Before publishing

1. Add the CV as `assets/Jabez_Magomere_CV.pdf`, then replace the disabled CV navigation label with `<a href="assets/Jabez_Magomere_CV.pdf">CV</a>`.
2. Add the final site URL to `og:url` and use an absolute URL for `og:image` once the domain is known.
3. Replace the INCLUDE-2.0 collaboration line with the full author list and add the paper link when public.

## Deploy

The folder can be deployed directly to GitHub Pages, Netlify, Cloudflare Pages, or any static host. No build command is required.
