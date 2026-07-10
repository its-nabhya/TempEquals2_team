"""
Regex-based Named Entity Recognition solver.
"""

from __future__ import annotations

import re


PERSON = re.compile(
    r"\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b"
)

ORG = re.compile(
    r"\b(OpenAI|Fireworks AI|Google|Microsoft|Apple|Meta|Amazon)\b"
)

LOCATION = re.compile(
    r"\b(Berlin|London|Paris|Tokyo|Sydney|Delhi|Mumbai|New York)\b"
)

DATE = re.compile(
    r"\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\b"
)


def solve_ner(
    prompt: str,
) -> tuple[dict | None, float]:

    entities = {}

    persons = PERSON.findall(prompt)
    orgs = ORG.findall(prompt)
    locations = LOCATION.findall(prompt)
    dates = DATE.findall(prompt)

    if persons:
        entities["person"] = persons

    if orgs:
        entities["organization"] = orgs

    if locations:
        entities["location"] = locations

    if dates:
        entities["date"] = dates

    if not entities:
        return None, 0.0

    return entities, 0.95