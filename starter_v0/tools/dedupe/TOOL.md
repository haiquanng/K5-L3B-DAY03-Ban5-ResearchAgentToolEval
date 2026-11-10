---
name: dedupe
track: bonus
kind: local_formatter
requires_env: []
inputs: [items, key]
outputs: [items, count, removed]
side_effect: false
---
# dedupe

Remove duplicate results (same article from two searches) before building a digest with `format`.

- `items`: list of objects (up to 500) such as `{title, url, source, summary}`; the input list is not modified.
- `key`: `url` (default) or `title`.
  - URLs match ignoring case of the host, `www.`, trailing `/`, `#fragment`, `utm_*` and similar tracking parameters.
  - Titles match ignoring case, accents and punctuation.
- The first occurrence is kept. Items without the chosen field are kept as they are.
- Success: `{tool, key, items, count, removed}`. Failure (not a list, non-object items, bad key, too many items): `{tool, error, message}`.

Not a search tool: it only cleans a list that is already available.
