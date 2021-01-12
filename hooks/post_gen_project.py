import logging
from pathlib import Path
from typing import Literal
import os

logger = logging.getLogger(__name__)


def rm_non_gitkeep(folder: Literal["great_expectations", "tests"]):
    path = Path("code/python" / folder)
    for f in path.iterdir():
        if f.is_file() and f.stem != ".gitkeep":
            f.unlink()


def main():
    rm_non_gitkeep(folder="tests")
    rm_non_gitkeep(folder="great_expectations")


if __name__ == "__main__":
    main()
