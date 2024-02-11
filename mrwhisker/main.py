from typing import Union
from io import TextIOWrapper


def render(template: Union[str, TextIOWrapper]) -> str:
    if isinstance(template, TextIOWrapper):
        template = template.read()
    return template
