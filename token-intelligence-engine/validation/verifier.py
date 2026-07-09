"""
Response verification.

Version 1 performs only minimal validation.
"""

from schemas.context import TaskContext


def verify(
    context: TaskContext,
) -> bool:
    """
    Verify the generated response.

    Returns
    -------
    bool
        True if the response is considered valid.
    """

    return context.answer is not None