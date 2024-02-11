import re
from typing import Union
from io import TextIOWrapper


def render(template: Union[str, TextIOWrapper], data: str = None) -> str:
    """
    Render a mustache template

    Args:
    template (str, TextIOWrapper): The template to render. This can be either a string or a TextIOWrapper object.
    data (dict, str): The data to use for rendering the template. This is an optional arg. This can be either a dictionary or a string.

    Returns:
    str: The rendered template.
    """
    if not isinstance(template, (str, TextIOWrapper)):
        raise TypeError("Template must be of type string or TextIOWrapper")

    if isinstance(template, TextIOWrapper):
        template = template.read()

    if not data:
        data = ''

    if isinstance(data, str) and data.isspace():
        data = ''

    if isinstance(data, str):
        template = re.sub(r'{{\s*(\w+)\s*}}', data, template)

    tokens = set(re.findall(r'{{\s*(\w+)\s*}}', template))

    if data and isinstance(data, dict):
      tokens.update(data.keys())
      for token in tokens:
          value = data.get(token, '')
          template = re.sub(r'{{\s*%s\s*}}' % token, value, template)
    return template
