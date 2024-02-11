from typing import Union
from io import TextIOWrapper


def render(template: Union[str, TextIOWrapper]) -> str:
    """
    Render a mustache template
    """
    if not isinstance(template, (str, TextIOWrapper)):
        raise TypeError("Template must be a string or file object")

    if isinstance(template, TextIOWrapper):
        template = template.read()
    return template
