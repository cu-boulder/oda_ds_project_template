import logging
from pathlib import Path
from typing import Literal
import os

logger = logging.getLogger(__name__)


def rm_non_gitkeep(path: Path):
    if not path.is_dir():
        raise FileNotFoundError(f"{path} is not a valid directory")
    for f in path.iterdir():
        if f.is_file() and f.stem != ".gitkeep":
            f.unlink()


def main():
    rm_non_gitkeep(Path(f"code/python/tests")
    rm_non_gitkeep(Path(f"code/python/great_expectations/expectations")


if __name__ == "__main__":
    main()
