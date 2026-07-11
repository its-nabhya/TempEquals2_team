from constants.task_type import TaskType


USE_SYMBOLIC = "symbolic"
USE_LOCAL = "local"
USE_FIREWORKS = "fireworks"


ROUTING_POLICY = {

    TaskType.MATH:
        USE_SYMBOLIC,

    TaskType.SENTIMENT:
        USE_SYMBOLIC,

    TaskType.NER:
        USE_SYMBOLIC,

    TaskType.FACTUAL:
        USE_LOCAL,

    TaskType.SUMMARIZATION:
        USE_FIREWORKS,

    TaskType.LOGICAL_REASONING:
        USE_FIREWORKS,

    TaskType.CODE_GENERATION:
        USE_FIREWORKS,

    TaskType.CODE_DEBUGGING:
        USE_FIREWORKS,
}
