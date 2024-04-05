import logging
import logging.config
from pathlib import Path

import yaml

__all__ = [
    'setup_logging'
]


def setup_logging() -> None:
    """Setup logging"""
    config_file = Path(__file__).resolve().parent.parent / 'resources' / 'logging.config.yaml'

    with config_file.open('r') as config_stream:
        config = yaml.load(config_stream, yaml.SafeLoader)

    logging.config.dictConfig(config)
    logging.getLogger().setLevel(logging.DEBUG)
