"""
Prompt canonicalization.

Version 1 intentionally performs no transformations.
Future versions will normalize prompts to improve routing and
token efficiency.
"""

from schemas.context import TaskContext


def canonicalize(
    context: TaskContext,
) -> None:
    """
    Canonicalize the task prompt.

    Currently a no-op.
    """

    context.canonical_prompt = context.task.prompt