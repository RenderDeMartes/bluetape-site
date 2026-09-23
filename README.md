# bluetaperigging.com — 2026 redesign (local)

Static site, no build step. `python gen.py` regenerates every page from the partials in
`gen.py`; the HTML files are output. Preview with `python -m http.server 8793` in this folder
(paths are root-relative, so opening the files directly from disk won't load assets).

Pages: `/`, `/services/`, `/work/`, `/approach/`, `/contact/`, plus 8 search landing pages whose
copy lives in `seo_pages.py` (linked from the footer and the services rows). `gen.py` also
writes `sitemap.xml` and `robots.txt`.

## Rules carried over from the previous brief
- No individual is named anywhere on the site. The studio speaks as "we".
- Any rig system: the client's own, mGear, hand-built, a new one, or Mutant Tools. Mutant Tools is
  one option, not the headline (2026-09-23).
- Every credit is real; free assets are "in audit" with no date.

## Still to confirm before going live
- `hello@bluetaperigging.com` is a placeholder (set in `assets/js/site.js`).
- The contact form opens the visitor's mail app (mailto), no server.
- Schweppes still is hotlinked from YouTube (`THUMB` in gen.py); self-host a still to drop it.
