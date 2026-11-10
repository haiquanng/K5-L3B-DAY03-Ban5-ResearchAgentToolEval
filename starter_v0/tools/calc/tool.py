"""Safe arithmetic calculator: parses the expression itself, never calls eval()."""
from __future__ import annotations

import ast
import math
import operator
from typing import Any

from tools._shared import err

MAX_EXPRESSION_LENGTH = 200
MAX_EXPONENT = 100
MAX_RESULT_BITS = 20000
MAX_DEPTH = 40

_BINARY = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}
_UNARY = {ast.UAdd: operator.pos, ast.USub: operator.neg}


def _evaluate(node: ast.AST, depth: int = 0) -> int | float:
    if depth > MAX_DEPTH:
        raise ValueError("expression is nested too deeply")
    if isinstance(node, ast.Expression):
        return _evaluate(node.body, depth + 1)
    if isinstance(node, ast.Constant):
        if type(node.value) in (int, float):  # rejects bool, str, None, complex
            return node.value
        raise ValueError("only plain numbers are allowed")
    if isinstance(node, ast.UnaryOp) and type(node.op) in _UNARY:
        return _UNARY[type(node.op)](_evaluate(node.operand, depth + 1))
    if isinstance(node, ast.BinOp) and type(node.op) in _BINARY:
        left = _evaluate(node.left, depth + 1)
        right = _evaluate(node.right, depth + 1)
        if isinstance(node.op, ast.Pow):
            if abs(right) > MAX_EXPONENT:
                raise ValueError(f"exponent must be between -{MAX_EXPONENT} and {MAX_EXPONENT}")
            if isinstance(left, int) and isinstance(right, int) and right > 0 and left.bit_length() * right > MAX_RESULT_BITS:
                raise ValueError("result is too large")
        result = _BINARY[type(node.op)](left, right)
        if isinstance(result, complex):
            raise ValueError("result is not a real number")
        return result
    raise ValueError("unsupported syntax: use only numbers, + - * / // % ** and parentheses")


def calculate(expression: str = "") -> dict[str, Any]:
    """Evaluate one arithmetic expression; malformed or unsafe input returns an error dict."""
    try:
        if not isinstance(expression, str) or not expression.strip():
            raise ValueError("expression must be a non-empty string")
        if len(expression) > MAX_EXPRESSION_LENGTH:
            raise ValueError(f"expression is longer than {MAX_EXPRESSION_LENGTH} characters")
        cleaned = expression.strip().replace("×", "*").replace("÷", "/").replace("^", "**")
        value = _evaluate(ast.parse(cleaned, mode="eval"))
        if isinstance(value, float) and not math.isfinite(value):
            raise ValueError("result must be finite")
        return {"tool": "calc", "expression": expression.strip(), "value": value}
    except SyntaxError as exc:
        return err("calc", ValueError(f"invalid expression: {exc.msg}"))
    except Exception as exc:
        return err("calc", exc)
