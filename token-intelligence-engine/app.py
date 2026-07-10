"""
Application entry point.

This module is responsible only for bootstrapping the application.

Responsibilities:
    1. Load application configuration.
    2. Configure logging.
    3. Read input tasks.
    4. Construct the processing pipeline.
    5. Execute the pipeline.
    6. Persist output results.
    7. Exit with the appropriate status code.

Business logic should NEVER be implemented in this file.
"""

import logging
import sys

from config import load_config
from core.io import load_tasks, save_results
from core.pipeline import Pipeline
from inference.factory import ProviderFactory
from routing.router import Router
from utils.logger import configure_logging
from validation.startup import validate_startup

logger = logging.getLogger(__name__)


def main() -> int:
    """
    Application entry point.

    Returns
    -------
    int
        0 on successful execution.
        Non-zero on failure.
    """

    try:
        # ------------------------------------------------------------------
        # Load application configuration
        # ------------------------------------------------------------------
        config = load_config()
        
        # ------------------------------------------------------------------
        # Validate startup configuration
        # ------------------------------------------------------------------
        validate_startup(config)

        logger.info("Configuration:")
        logger.info("  Provider      : %s", config.provider)
        logger.info("  Input Path    : %s", config.input_path)
        logger.info("  Output Path   : %s", config.output_path)
        logger.info("  Allowed Models: %s", config.allowed_models)
        # ------------------------------------------------------------------
        # Configure logging
        # ------------------------------------------------------------------
        configure_logging(config.log_level)

        logger.info("Application started.")

        # ------------------------------------------------------------------
        # Load input tasks
        # ------------------------------------------------------------------
        tasks = load_tasks(config.input_path)

        logger.info("Loaded %d task(s).", len(tasks))

        # ------------------------------------------------------------------
        # Build core components
        # ------------------------------------------------------------------
        router = Router(config)

        provider = ProviderFactory.create(config)

        pipeline = Pipeline(
            router=router,
            provider=provider,
        )

        # ------------------------------------------------------------------
        # Execute processing pipeline
        # ------------------------------------------------------------------
        results = pipeline.run(tasks)

        # ------------------------------------------------------------------
        # Persist results
        # ------------------------------------------------------------------
        save_results(results, config.output_path)

        logger.info("Successfully processed all tasks.")

        return 0

    except Exception:
        logger.exception("Fatal application error.")
        return 1


if __name__ == "__main__":
    sys.exit(main())