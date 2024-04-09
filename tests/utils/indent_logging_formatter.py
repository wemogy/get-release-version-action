from textwrap import indent
from logging import Formatter
from typing import override

__all__ = [
    'IndentLoggingFormatter'
]


class IndentLoggingFormatter(Formatter):
    def __init__(self, fmt):
        super().__init__(fmt)

    @override
    def format(self, record):
        msg = super().format(record)
        return indent(msg, '    ', predicate=lambda line: line != msg.splitlines(keepends=True)[0])
