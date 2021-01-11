import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def remove_test_files():
    logger.info("Removing test files")
    tests = (
        Path(__file__).resolve().parents[0]
        / "{{cookiecutter.project_name}}/code/python/tests"
    )
    for f in tests.iterdir():
        if f.is_file() and ".gitkeep" not in tests.stem:
            f.unlink()


def main():
    remove_test_files()


if __name__ == "__main__":
    main()