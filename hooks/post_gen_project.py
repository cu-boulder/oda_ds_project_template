from pathlib import Path

logger = logging.getLogger(__name__)


def remove_test_files():
    logger.info("Removing test files")
    tests = Path("/code/python/tests")
    [
        f.unlink()
        for f in tests.glob("*")
        if f.is_file() and ".gitkeep" not in tests.stem
    ]


def main():
    remove_test_files()