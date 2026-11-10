---
name: calc
track: bonus
kind: local_formatter
requires_env: []
inputs: [expression]
outputs: [expression, value]
side_effect: false
---
# calc

Evaluate one arithmetic expression exactly, without `eval()`. The tool parses the text itself and
only accepts numbers, `+ - * / // % **` (also `^`, `×`, `÷`) and parentheses.

- `expression`: at most 200 characters; names, function calls, strings and attributes are rejected.
- Exponents are limited to ±100 and huge results are refused, so a bad input cannot hang the agent.
- Success: `{tool, expression, value}`.
- Failure (empty input, bad syntax, division by zero, unsupported syntax): `{tool, error, message}`; nothing is raised.

Example: `calc(expression="(1250 + 380) * 12 / 4")` returns `value=4890.0`.
Not for word problems or algebra/calculus; for a list of numbers use `stats`.
