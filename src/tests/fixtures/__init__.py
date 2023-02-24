import json
import pathlib
from typing import Union


PARENT_DIR = pathlib.Path(__file__).parent.absolute()


def read(filename: str) -> Union[str, dict, list]:
    with open(PARENT_DIR / filename) as f:
        return json.load(f)
