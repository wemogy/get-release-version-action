"""Utils for logging."""
import logging
import logging.config
from pathlib import Path
from textwrap import indent
from typing import override

import yaml

__all__ = [
    'IndentLoggingFormatter',
    'setup_logging'
]


class IndentLoggingFormatter(logging.Formatter):
    """Logging formatter to indent multiline messages."""

    def __init__(self, fmt: str | None) -> None:
        super().__init__(fmt)

    @override
    def format(self, record: logging.LogRecord) -> str:
        msg = super().format(record)
        return indent(msg, '    ', predicate=lambda line: line != msg.splitlines(keepends=True)[0])


def setup_logging(debug: bool) -> None:
    """Setup logging."""
    config_file = Path(__file__).resolve().parent.parent.parent / 'resources' / 'logging.config.yaml'

    with config_file.open('r') as config_stream:
        config = yaml.load(config_stream, yaml.SafeLoader)

    logging.config.dictConfig(config)
    logging.getLogger().setLevel(logging.DEBUG if debug else logging.INFO)
