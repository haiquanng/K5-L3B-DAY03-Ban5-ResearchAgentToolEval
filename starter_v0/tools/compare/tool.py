"""Compare two numbers: difference, percent change and which one is larger."""
from __future__ import annotations

import math
from typing import Any

from tools._shared import err

MAX_LABEL_LENGTH = 50


def _number(name: str, value: Any) -> float | int:
    if type(value) not in (int, float) or not math.isfinite(value):
        raise ValueError(f"{name} must be a finite number (not a string or boolean)")
    return value


def _label(name: str, value: Any) -> str:
    if not isinstance(value, str) or not value.strip() or len(value) > MAX_LABEL_LENGTH:
        raise ValueError(f"{name} must be a short non-empty string")
    return value.strip()


def compare_values(a: float | None = None, b: float | None = None, label_a: str = "A", label_b: str = "B") -> dict[str, Any]:
    """Describe how b differs from a. Percent change is relative to |a| and null when a is 0."""
    try:
        first, second = _number("a", a), _number("b", b)
        name_a, name_b = _label("label_a", label_a), _label("label_b", label_b)
        difference = second - first
        percent = None if first == 0 else round(difference / abs(first) * 100, 4)
        ratio = None if first == 0 else round(second / first, 6)
        larger = "equal" if first == second else (name_a if first > second else name_b)
        return {
            "tool": "compare",
            "a": first,
            "b": second,
            "difference": difference,
            "percent_change": percent,
            "ratio": ratio,
            "larger": larger,
        }
    except Exception as exc:
        return err("compare", exc)
