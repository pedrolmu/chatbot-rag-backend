import logging
import sys


def configure_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format='{"level":"%(levelname)s","module":"%(name)s","message":"%(message)s"}',
        handlers=[logging.StreamHandler(sys.stdout)],
    )
