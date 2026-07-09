"""
Local symbolic inference engine.
"""

from __future__ import annotations

from constants.task_type import TaskType
from schemas.context import TaskContext

from analysis.solvers.math_solver import solve_math
from analysis.solvers.sentiment_solver import solve_sentiment


def solve(
    context: TaskContext,
) -> None:
    """
    Attempt to solve the task locally.

    The function updates the TaskContext in-place.
    """

    if context.task_type is TaskType.MATH:

        answer, confidence = solve_math(
            context.task.prompt
        )

        if confidence >= 0.99:

            context.local_answer = answer
            context.confidence = confidence
            context.solved_locally = True

        return

    if context.task_type is TaskType.SENTIMENT:

        answer, confidence = solve_sentiment(
            context.task.prompt
        )

        if confidence >= 0.95:

            context.local_answer = answer
            context.confidence = confidence
            context.solved_locally = True