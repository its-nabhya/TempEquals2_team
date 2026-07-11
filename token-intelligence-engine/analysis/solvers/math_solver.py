from __future__ import annotations

import ast
import math
import operator
import re
from fractions import Fraction

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

    raise ValueError("Unsupported AST node")


def safe_eval(expr: str):
    # Support exponentiation syntax and superscript mapping
    expr = expr.replace("^", "**").replace("³", "**3").replace("²", "**2")
    
    tree = ast.parse(
        expr,
        mode="eval",
    )

    return _eval(tree.body)


def solve_math(prompt):
    text = prompt.lower()

    # -----------------------------
    # Evaluate (...) / Parentheses / Exponents
    # -----------------------------
    m = re.search(
        r"evaluate\s*:?\s*([\(\d][\d\.\+\-\*/\(\)\^\s]+)",
        text,
    )
    if m:
        try:
            return (
                str(safe_eval(m.group(1).strip())),
                1.0,
            )
        except Exception:
            pass

    # -----------------------------
    # Roots and Specific Exponents
    # -----------------------------
    m = re.search(r"(?:square\s+root\s+of|sqrt\s*\()\s*(\d+(?:\.\d+)?)\)?", text)
    if m:
        return (f"{math.sqrt(float(m.group(1))):g}", 1.0)

    m = re.search(r"cube\s+of\s+(\d+(?:\.\d+)?)", text)
    if m:
        return (f"{float(m.group(1)) ** 3:g}", 1.0)

    m = re.search(r"square\s+of\s+(\d+(?:\.\d+)?)", text)
    if m:
        return (f"{float(m.group(1)) ** 2:g}", 1.0)

    # -----------------------------
    # Simple Interest
    # -----------------------------
    m = re.search(
        r"simple\s+interest.*?(?:principal|p)[\s=:]*(\d+(?:\.\d+)?).*?(?:rate|r)[\s=:]*(\d+(?:\.\d+)?).*?(?:time|t)[\s=:]*(\d+(?:\.\d+)?)",
        text,
    )
    if m:
        p, r, t = map(float, m.groups())
        si = (p * r * t) / 100
        return (
            str(int(si) if si.is_integer() else round(si, 4)),
            1.0,
        )

    # -----------------------------
    # Compound Interest
    # -----------------------------
    m = re.search(
        r"compound\s+interest.*?(?:principal|p)[\s=:]*(\d+(?:\.\d+)?).*?(?:rate|r)[\s=:]*(\d+(?:\.\d+)?).*?(?:time|t)[\s=:]*(\d+(?:\.\d+)?)",
        text,
    )
    if m:
        p, r, t = map(float, m.groups())
        amount = p * ((1 + (r / 100)) ** t)
        ci = amount - p
        return (
            str(int(ci) if ci.is_integer() else round(ci, 4)),
            1.0,
        )

    # -----------------------------
    # Rectangle Area
    # -----------------------------
    m = re.search(
        r"area\s+of.*?(?:rectangle|rect).*?length[\s=:]*(\d+(?:\.\d+)?).*?width[\s=:]*(\d+(?:\.\d+)?)",
        text,
    )
    if m:
        l, w = map(float, m.groups())
        area = l * w
        return (
            str(int(area) if area.is_integer() else area),
            1.0,
        )

    # -----------------------------
    # Circle Area
    # -----------------------------
    m = re.search(
        r"radius[\s=:]*(\d+(?:\.\d+)?)",
        text,
    )
    if m and "area" in text:
        r = float(m.group(1))
        pi = 3.1415926535
        m2 = re.search(r"pi\s*=\s*(\d+(?:\.\d+)?)", text)
        if m2:
            pi = float(m2.group(1))
            
        area = pi * (r ** 2)
        # Strips trailing zeros/decimals naturally
        return (
            f"{area:.2f}".rstrip("0").rstrip("."),
            1.0,
        )

    # -----------------------------
    # Profit / Loss
    # -----------------------------
    m = re.search(
        r"(?:cost\s+price|cp)[\s=:]*(\d+(?:\.\d+)?).*?(?:selling\s+price|sp)[\s=:]*(\d+(?:\.\d+)?)",
        text,
    )
    if m:
        cp, sp = map(float, m.groups())
        diff = sp - cp
        status = "profit" if diff > 0 else ("loss" if diff < 0 else "break-even")
        return (
            f"{status}: {abs(diff):g}",
            1.0,
        )

    # -----------------------------
    # Averages
    # -----------------------------
    m = re.search(
        r"average\s+of\s+([\d\.\s,and]+)",
        text,
    )
    if m:
        nums = re.findall(r"(\d+(?:\.\d+)?)", m.group(1))
        if nums:
            parsed_nums = [float(n) for n in nums]
            avg = sum(parsed_nums) / len(parsed_nums)
            return (
                str(int(avg) if avg.is_integer() else round(avg, 4)),
                1.0,
            )

    # -----------------------------
    # Ratios
    # -----------------------------
    m = re.search(
        r"ratio\s+of\s+(\d+(?:\.\d+)?)\s*(?:to|:|and)\s*(\d+(?:\.\d+)?)",
        text,
    )
    if m:
        n1, n2 = float(m.group(1)), float(m.group(2))
        if n2 != 0:
            if n1.is_integer() and n2.is_integer():
                frac = Fraction(int(n1), int(n2))
            else:
                frac = Fraction(n1 / n2).limit_denominator(1000)
                
            return (
                f"{frac.numerator}:{frac.denominator}",
                1.0,
            )

    # -----------------------------
    # Percentage (Increase/Decrease/Modifiers)
    # -----------------------------
    # 1. Increase / Decrease logic (X by Y%)
    m = re.search(r"(increase|decrease|reduce)\s+(\d+(?:\.\d+)?)\s+(?:by\s+)?(\d+(?:\.\d+)?)%", text)
    if m:
        action, val, pct = m.group(1), float(m.group(2)), float(m.group(3))
        ans = val * (1 - pct/100) if action in ("decrease", "reduce") else val * (1 + pct/100)
        return (f"{ans:g}", 1.0)

    # 2. Tax / GST / Tip (Add to total)
    m = re.search(r"(?:tax|gst|tip)\s+(?:of\s+)?(\d+(?:\.\d+)?)%\s+(?:on|of)\s+(\d+(?:\.\d+)?)", text)
    if not m:
        m = re.search(r"(\d+(?:\.\d+)?)%\s+(?:tax|gst|tip)\s+(?:on|of)\s+(\d+(?:\.\d+)?)", text)
    if m:
        pct, val = map(float, m.groups())
        ans = val * (1 + pct/100)
        return (f"{ans:g}", 1.0)

    # 3. Discount / Loss (Subtract from total)
    m = re.search(r"(?:discount|loss)\s+(?:of\s+)?(\d+(?:\.\d+)?)%\s+(?:on|of)\s+(\d+(?:\.\d+)?)", text)
    if not m:
        m = re.search(r"(\d+(?:\.\d+)?)%\s+(?:discount|loss)\s+(?:on|of)\s+(\d+(?:\.\d+)?)", text)
    if m:
        pct, val = map(float, m.groups())
        ans = val * (1 - pct/100)
        return (f"{ans:g}", 1.0)

    # 4. Standard Percentage (X% of Y)
    m = re.search(
        r"(\d+(?:\.\d+)?)%\s+of\s+(\d+(?:\.\d+)?)",
        text,
    )
    if m:
        pct = float(m.group(1))
        value = float(m.group(2))
        result = value * (pct / 100)
        return (
            f"{result:g}",
            1.0,
        )

    # -----------------------------
    # Speed × Time = Distance
    # -----------------------------
    m = re.search(
        r"(\d+(?:\.\d+)?)\s*(mph|km/h|m/s).*?(\d+(?:\.\d+)?)\s*(?:hours?|hrs?|seconds?|secs?|minutes?|mins?)",
        text,
    )
    if m:
        speed = float(m.group(1))
        unit_str = m.group(2)
        time = float(m.group(3))
        d = speed * time
        
        unit = "units"
        if "mph" in unit_str:
            unit = "miles"
        elif "km/h" in unit_str:
            unit = "km"
        elif "m/s" in unit_str:
            unit = "meters"

        return (
            f"{d:g} {unit}",
            1.0,
        )

    # -----------------------------
    # Solve for x (Linear equation)
    # -----------------------------
    # Matches +/-ax +/- b = c OR ax = c OR x = c
    m = re.search(
        r"(-?\d+(?:\.\d+)?)?x\s*([+-])?\s*(\d+(?:\.\d+)?)?\s*=\s*(-?\d+(?:\.\d+)?)",
        text,
    )
    if m:
        a_str, sign, b_str, c_str = m.groups()
        
        if not a_str or a_str == "+":
            a = 1.0
        elif a_str == "-":
            a = -1.0
        else:
            a = float(a_str)
            
        c = float(c_str)
        b = float(b_str) if b_str else 0.0

        if sign == "+":
            x = (c - b) / a
        elif sign == "-":
            x = (c + b) / a
        else:
            x = c / a

        return (
            str(int(x) if x.is_integer() else round(x, 4)),
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

    # -----------------------------
    # Basic arithmetic / Fractions / Fallback Evaluator
    # -----------------------------
    # Regex ensures string has a digit/parenthesis and ignores completely blank/text queries
    m = re.search(
        r"([\(\d][\d\.\+\-\*/\(\)\^\s]*[\d\)])",
        text,
    )
    if m:
        expr = m.group(1).strip()
        # Verify it actually has an operation so we don't evaluate singular integers
        if any(op in expr for op in "+-*/^()"):
            try:
                return (
                    str(safe_eval(expr)),
                    1.0,
                )
            except Exception:
                pass

    return (
        None,
        0.0,
    )
# from __future__ import annotations

# import ast
# import math
# import operator
# import re

# OPS = {
#     ast.Add: operator.add,
#     ast.Sub: operator.sub,
#     ast.Mult: operator.mul,
#     ast.Div: operator.truediv,
#     ast.Pow: operator.pow,
#     ast.Mod: operator.mod,
#     ast.USub: operator.neg,
# }


# def _eval(node):

#     if isinstance(node, ast.Constant):
#         return node.value

#     if isinstance(node, ast.UnaryOp):
#         return OPS[type(node.op)](
#             _eval(node.operand)
#         )

#     if isinstance(node, ast.BinOp):
#         return OPS[type(node.op)](
#             _eval(node.left),
#             _eval(node.right),
#         )

#     raise ValueError


# def safe_eval(expr: str):

#     tree = ast.parse(
#         expr,
#         mode="eval",
#     )

#     return _eval(tree.body)


# def solve_math(prompt):

#     text = prompt.lower()

#     # -----------------------------
#     # Evaluate (...)
#     # -----------------------------

#     m = re.search(
#         r"evaluate\s*:?\s*([0-9\.\+\-\*/\(\)\s]+)",
#         text,
#     )

#     if m:

#         try:

#             return (
#                 str(safe_eval(m.group(1))),
#                 1.0,
#             )

#         except Exception:
#             pass

#     # -----------------------------
#     # Basic arithmetic
#     # -----------------------------

#     m = re.search(
#         r"([0-9\.\+\-\*/\(\)\s]+)",
#         text,
#     )

#     if m:

#         expr = m.group(1).strip()

#         if any(
#             op in expr
#             for op in "+-*/"
#         ):

#             try:

#                 return (
#                     str(safe_eval(expr)),
#                     1.0,
#                 )

#             except Exception:
#                 pass

#     # -----------------------------
#     # Percentage
#     # -----------------------------

#     m = re.search(
#         r"(\d+(?:\.\d+)?)%\s+of\s+(\d+(?:\.\d+)?)",
#         text,
#     )

#     if m:

#         pct = float(m.group(1))

#         value = float(m.group(2))

#         return (
#             str(value * pct / 100),
#             1.0,
#         )

#     # -----------------------------
#     # Linear equation
#     # -----------------------------

#     m = re.search(
#         r"(\d+)x\s*([+-])\s*(\d+)\s*=\s*(-?\d+)",
#         text,
#     )

#     if m:

#         a = int(m.group(1))

#         sign = m.group(2)

#         b = int(m.group(3))

#         c = int(m.group(4))

#         if sign == "+":
#             x = (c - b) / a
#         else:
#             x = (c + b) / a

#         return (
#             str(int(x) if x.is_integer() else x),
#             1.0,
#         )

#     # -----------------------------
#     # Speed × Time
#     # -----------------------------

#     m = re.search(
#         r"(\d+(?:\.\d+)?)\s*mph.*?(\d+(?:\.\d+)?)\s*hours",
#         text,
#     )

#     if m:

#         d = float(m.group(1)) * float(m.group(2))

#         return (
#             f"{d:g} miles",
#             1.0,
#         )

#     # -----------------------------
#     # Circle area
#     # -----------------------------

#     m = re.search(
#         r"radius\s*(\d+(?:\.\d+)?)",
#         text,
#     )

#     if m and "area" in text:

#         r = float(m.group(1))

#         pi = 3.14

#         m2 = re.search(
#             r"pi\s*=\s*(\d+(?:\.\d+)?)",
#             text,
#         )

#         if m2:
#             pi = float(m2.group(1))

#         area = pi * r * r

#         return (
#             f"{area:.2f}",
#             1.0,
#         )

#     # -----------------------------
#     # Factorial
#     # -----------------------------

#     m = re.search(
#         r"factorial\s+of\s+(\d+)",
#         text,
#     )

#     if m:

#         return (
#             str(math.factorial(int(m.group(1)))),
#             1.0,
#         )

#     return (
#         None,
#         0.0,
#     )