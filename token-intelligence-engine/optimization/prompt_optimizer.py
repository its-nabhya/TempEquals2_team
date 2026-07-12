"""
Prompt optimization.
"""

from constants.task_type import TaskType


def optimize_prompt(
    prompt: str,
    task_type: TaskType,
) -> str:

    if task_type is TaskType.FACTUAL:

        return (
            "Return ONLY the answer in ONE sentence.\n"
            "Do not explain.\n\n"
            f"{prompt}"
        )

    if task_type is TaskType.MATH:

        return (
            "Solve carefully.\n"
            "Return ONLY the final answer.\n"
            "No explanation.\n\n"
            f"{prompt}"
        )

    if task_type is TaskType.SENTIMENT:

        return (
            "Classify the sentiment.\n" 
            "Return ONLY ONE WORD FROM:.\n"
            "Positive\n"
            "Negative\n"
            "Neutral\n"
            "Mixed\n\n"
            f"{prompt}"
        )

    if task_type is TaskType.NER:

        return (
            "Extract all entities.\n"
            "Return ONLY valid JSON.\n\n"
            "{\n"
            '  "person": [],\n'
            '  "organization": [],\n'
            '  "location": [],\n'
            '  "date": []\n'
            '  "event":[]\n'
            "}\n\n"
            f"{prompt}"
        )

    if task_type is TaskType.SUMMARIZATION:

        return (
            "Summarize in ONE sentence. Print ONLY Summary\n"
            "Do not explain.\n\n"
            f"{prompt}"
        )

    if task_type is TaskType.CODE_GENERATION:

        return (
            "Return ONLY code. DO NOT SHOW THINKING\n"
            "No markdown.\n"
            "No explanation.\n\n"
            f"{prompt}"
        )

    if task_type is TaskType.CODE_DEBUGGING:

        return (
            "Find the bug.\n"
            "Return ONLY the corrected code.\n"
            "No explanation.\n\n"
            f"{prompt}"
        )

    if task_type is TaskType.LOGICAL_REASONING:

        return (
            "Reason carefully. DO NOT SHOW THINKING.\n"
            "Return ONLY the final answer.\n"
            "Keep it concise.\n\n"
            f"{prompt}"
        )

    return prompt