import logging
import sys


def configure_logging(level: str) -> None:
    """Configure application-wide logging with a simple structured format."""
    logging.basicConfig(
        level=level.upper(),
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
        force=True,
    )
