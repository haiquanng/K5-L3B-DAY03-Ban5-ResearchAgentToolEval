---
name: compare
track: bonus
kind: local_formatter
requires_env: []
inputs: [a, b, label_a, label_b]
outputs: [a, b, difference, percent_change, ratio, larger]
side_effect: false
---
# compare

Compare two numbers the user already gave (for example this month vs last month).

- `a` is the baseline and `b` the new value: `difference = b - a`, `percent_change = (b - a) / |a| * 100`.
- `percent_change` and `ratio` are `null` when `a` is 0 (no meaningful percentage).
- `larger` is the label of the bigger value, or `"equal"`.
- Inputs must be finite numbers; strings, booleans, NaN and Infinity return an error dict.

Example: `compare(a=1000, b=1200)` returns `percent_change=20.0`.
Not for lists of numbers (`stats`) or general arithmetic (`calc`).
