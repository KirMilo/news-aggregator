__all__ = [
    "PARSERS_CLASSES",
    "ParserInterface",
]

from pathlib import Path
from importlib import import_module
from .interfaces import ParserInterface

PARSERS_CLASSES = []

path = Path(__file__).parent

for parser_dir in (file for file in path.iterdir() if file.is_dir() and file.name != "__pycache__"):
    try:
        module = import_module(f"{path.name}.{parser_dir.name}.parser")
        PARSERS_CLASSES.append(module.Parser)
    except (ModuleNotFoundError, AttributeError):
        pass
