from pathlib import Path
from typing import Literal

logger = logging.getLogger(__name__)


def rm_non_gitkeep(path: Path):
    if not path.is_dir():
        raise FileNotFoundError(f"{path} is not a valid directory")
    for f in path.iterdir():
        if f.is_file() and f.stem != ".gitkeep":
            f.unlink()


def main():
    rm_non_gitkeep(Path("code/python/tests"))
    rm_non_gitkeep(Path("code/python/great_expectations/expectations"))


if __name__ == "__main__":
    main()
