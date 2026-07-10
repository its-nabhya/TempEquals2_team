"""
Local mathematical solver.
"""

from __future__ import annotations

import ast
import operator
import re

OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.USub: operator.neg,
}


def _eval(node):

    if isinstance(node, ast.Constant):
        return node.value

    if isinstance(node, ast.UnaryOp):
        return OPS[type(node.op)](
            _eval(node.operand)
        )

    if isinstance(node, ast.BinOp):
        return OPS[type(node.op)](
            _eval(node.left),
            _eval(node.right),
        )

    raise ValueError("Unsupported expression")


def safe_eval(expression: str):

    tree = ast.parse(
        expression,
        mode="eval",
    )

    return _eval(tree.body)


def solve_math(
    prompt: str,
) -> tuple[str | None, float]:

    prompt = prompt.lower()

    # ----------------------------------------------------
    # Arithmetic
    # ----------------------------------------------------

    match = re.search(
        r"(\d+(?:\.\d+)?(?:\s*[\+\-\*/]\s*\d+(?:\.\d+)?)+)",
        prompt,
    )

    if match:

        try:

            value = safe_eval(
                match.group(1)
            )

            return str(value), 1.0

        except Exception:
            pass

    # ----------------------------------------------------
    # Percentage
    # ----------------------------------------------------

    match = re.search(
        r"(\d+(?:\.\d+)?)%\s+of\s+(\d+(?:\.\d+)?)",
        prompt,
    )

    if match:

        pct = float(match.group(1))

        value = float(match.group(2))

        return str(value * pct / 100), 1.0

    return None, 0.0