"""Remove duplicate items (same URL or same title) from a list of search results."""
from __future__ import annotations

import re
from typing import Any
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from tools._shared import err, fold_text

MAX_ITEMS = 500
ALLOWED_KEYS = ("url", "title")
TRACKING_PARAMS = {"fbclid", "gclid", "mc_cid", "mc_eid", "ref", "ref_src", "igshid"}


def _normalize_url(value: str) -> str:
    parts = urlsplit(value.strip())
    host = parts.netloc.lower().removeprefix("www.")
    query = sorted(
        (k, v) for k, v in parse_qsl(parts.query, keep_blank_values=True)
        if not k.lower().startswith("utm_") and k.lower() not in TRACKING_PARAMS
    )
    path = parts.path.rstrip("/") or "/"
    return urlunsplit((parts.scheme.lower(), host, path, urlencode(query), ""))


def _normalize_title(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", fold_text(value)).strip()


def dedupe_items(items: list[dict[str, Any]] | None = None, key: str = "url") -> dict[str, Any]:
    """Keep the first item for each URL/title. Items without that field are kept untouched."""
    try:
        if not isinstance(items, list):
            raise ValueError("items must be a list of objects")
        if len(items) > MAX_ITEMS:
            raise ValueError(f"items has more than {MAX_ITEMS} entries")
        if key not in ALLOWED_KEYS:
            raise ValueError(f"key must be one of: {', '.join(ALLOWED_KEYS)}")
        if any(not isinstance(item, dict) for item in items):
            raise ValueError("every item must be an object with fields such as title and url")
        normalize = _normalize_url if key == "url" else _normalize_title
        seen: set[str] = set()
        unique: list[dict[str, Any]] = []
        for item in items:
            raw = item.get(key)
            normalized = normalize(raw) if isinstance(raw, str) and raw.strip() else ""
            if normalized and normalized in seen:
                continue
            if normalized:
                seen.add(normalized)
            unique.append(item)
        return {"tool": "dedupe", "key": key, "items": unique, "count": len(unique), "removed": len(items) - len(unique)}
    except Exception as exc:
        return err("dedupe", exc)
