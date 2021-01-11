import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def remove_test_files():
    logger.info("Removing test files")
    tests = Path("/code/python/tests")
    for f in tests.iterdir():
        print(f)
        print(type(f))
        # if f.is_file():
        #     f.unlink()


def main():
    remove_test_files()


if __name__ == "__main__":
    main()
