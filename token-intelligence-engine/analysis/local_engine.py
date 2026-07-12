"""
Local symbolic inference engine.
"""

from constants.task_type import TaskType
from schemas.context import TaskContext

from analysis.solvers.math_solver import solve_math
from analysis.solvers.sentiment_solver import solve_sentiment
from analysis.solvers.ner_solver import solve_ner

def solve(
    context: TaskContext,
) -> None:
    

    if context.task_type is TaskType.MATH:
        # print("Trying symbolic:", context.task_type)
        

        answer, confidence = solve_math(
            context.task.prompt
        )

        if confidence >= 0.99:

            context.local_answer = answer
            context.confidence = confidence
            context.local_solver = "math"
            context.solved_locally = True
        # print("Solved symbolically")
        return

    if context.task_type is TaskType.SENTIMENT:

        answer, confidence = solve_sentiment(
            context.task.prompt
        )

        if confidence >= 0.90:

            context.local_answer = answer
            context.confidence = confidence
            context.local_solver = "sentiment"
            context.solved_locally = True
    
    # if context.task_type is TaskType.NER:

    #     answer, confidence = solve_ner(
    #         context.task.prompt
    #     )

    #     if confidence >= 0.95:

    #         context.local_answer = answer
    #         context.confidence = confidence
    #         context.local_solver = "ner"
    #         context.solved_locally = True

    #     return