from __future__ import annotations

import ast
import math
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

    raise ValueError


def safe_eval(expr: str):

    tree = ast.parse(
        expr,
        mode="eval",
    )

    return _eval(tree.body)


def solve_math(prompt):

    text = prompt.lower()

    # -----------------------------
    # Evaluate (...)
    # -----------------------------

    m = re.search(
        r"evaluate\s*:?\s*([0-9\.\+\-\*/\(\)\s]+)",
        text,
    )

    if m:

        try:

            return (
                str(safe_eval(m.group(1))),
                1.0,
            )

        except Exception:
            pass

    # -----------------------------
    # Basic arithmetic
    # -----------------------------

    m = re.search(
        r"([0-9\.\+\-\*/\(\)\s]+)",
        text,
    )

    if m:

        expr = m.group(1).strip()

        if any(
            op in expr
            for op in "+-*/"
        ):

            try:

                return (
                    str(safe_eval(expr)),
                    1.0,
                )

            except Exception:
                pass

    # -----------------------------
    # Percentage
    # -----------------------------

    m = re.search(
        r"(\d+(?:\.\d+)?)%\s+of\s+(\d+(?:\.\d+)?)",
        text,
    )

    if m:

        pct = float(m.group(1))

        value = float(m.group(2))

        return (
            str(value * pct / 100),
            1.0,
        )

    # -----------------------------
    # Linear equation
    # -----------------------------

    m = re.search(
        r"(\d+)x\s*([+-])\s*(\d+)\s*=\s*(-?\d+)",
        text,
    )

    if m:

        a = int(m.group(1))

        sign = m.group(2)

        b = int(m.group(3))

        c = int(m.group(4))

        if sign == "+":
            x = (c - b) / a
        else:
            x = (c + b) / a

        return (
            str(int(x) if x.is_integer() else x),
            1.0,
        )

    # -----------------------------
    # Speed × Time
    # -----------------------------

    m = re.search(
        r"(\d+(?:\.\d+)?)\s*mph.*?(\d+(?:\.\d+)?)\s*hours",
        text,
    )

    if m:

        d = float(m.group(1)) * float(m.group(2))

        return (
            f"{d:g} miles",
            1.0,
        )

    # -----------------------------
    # Circle area
    # -----------------------------

    m = re.search(
        r"radius\s*(\d+(?:\.\d+)?)",
        text,
    )

    if m and "area" in text:

        r = float(m.group(1))

        pi = 3.14

        m2 = re.search(
            r"pi\s*=\s*(\d+(?:\.\d+)?)",
            text,
        )

        if m2:
            pi = float(m2.group(1))

        area = pi * r * r

        return (
            f"{area:.2f}",
            1.0,
        )

    # -----------------------------
    # Factorial
    # -----------------------------

    m = re.search(
        r"factorial\s+of\s+(\d+)",
        text,
    )

    if m:

        return (
            str(math.factorial(int(m.group(1)))),
            1.0,
        )

    return (
        None,
        0.0,
    )