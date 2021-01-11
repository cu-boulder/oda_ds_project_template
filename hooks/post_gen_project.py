import logging
from pathlib import Path
import os

logger = logging.getLogger(__name__)


def remove_test_files():
    logger.info("Removing test files")
    tests = Path("code/python/tests").resolve()
    for f in tests.iterdir():
        if f.is_file() and f.stem != ".gitkeep":
            f.unlink()


def main():
    remove_test_files()


if __name__ == "__main__":
    main()
