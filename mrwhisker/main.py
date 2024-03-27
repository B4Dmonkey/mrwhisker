import re
import html
from enum import Enum
from typing import Union, Generator
from io import TextIOWrapper

RAW_HTML_TOKEN_MATCHER = r'{{{\s*.*\s*}}}|{{&\s*.*\s*}}'


def render(template: Union[str, TextIOWrapper], data: Union[str, dict] = '') -> str:
    """
    Render a mustache template

    Args:
    template (str, TextIOWrapper): The template to render. This can be either a string or a TextIOWrapper object.
    data (str, dict): The data to use for rendering the template. This is an optional arg. This can be either a dictionary or a string.

    Returns:
    str: The rendered template.
    """
    assert isinstance(template, (str, TextIOWrapper)
                      ), "Template must be of type string or TextIOWrapper"
    assert isinstance(data, (str, dict)), "Data must be of type string or dict"

    if not data or isinstance(data, str) and data.isspace():
        data = ''

    if isinstance(template, TextIOWrapper):
        template = template.read()

    # * Find all the tokens in the template
    tokens = tokenize(template, data)

    for token in tokens:
        template = token.eval(template)

    return template


# TOKEN_MATCHER = r'({{2,3}\s*.*?\s*}{2,3})'
TOKEN_MATCHER = r'({{2,3}\s*\S*?\s*}{2,3})'


VARIABLE_TOKEN_MATCHER = r'{{\s*(\w+)\s*}}'
# RAW_HTML_TOKEN_MATCHER = r'{{{\s*(\w*)\s*}}}|{{&\s*(\w*)\s*}}'


class TokenType(Enum):
    VARIABLE = 'variable'
    RAW_HTML = 'raw_html'


class Token:
    def __init__(self, key: str, value: str):
        self._key = key
        self._value = value

    def eval(self, template: str) -> str:
        return template.replace(self._key, self._value)


def has_triple_mustache(value: str) -> bool:
    """
    Checks if a value has triple mustache
    Args:
    value (str): The value to check
    return (bool): True if the value has triple mustache, False otherwise
    """
    return '{{{' in value and '}}}' in value


def has_ampersand(value: str) -> bool:
    """
    Checks if a value has an ampersand
    Args:
    value (str): The value to check
    return (bool): True if the value has an ampersand, False otherwise
    """
    return '&' in value


def is_html_escape(value: str) -> bool:
    """
    Checks if a value is html escaped
    Args:
    value (str): The value to check
    return (bool): True if the value is html escaped, False otherwise
    """
    if has_triple_mustache(value):
        return False
    if has_ampersand(value):
        return False
    return True


def tokenize(template: str, data: Union[str, dict]) -> Generator[Token, None, None]:
    tokens = []
    for match in re.finditer(TOKEN_MATCHER, template):
        token_match = match.group()
        token_var = token_match.strip('{&}')
        token_value = data if isinstance(
            data, str) else data.get(token_var, '')

        if not token_value:
            token_value = ''

        # * convert int to string
        if isinstance(token_value, (int, float)):
            token_value = str(token_value)

        # * escape html characters
        if is_html_escape(token_match):
            token_value = html.escape(token_value)

        tokens.append(
            Token(key=token_match, value=token_value)
        )

    for token in tokens:
        yield token
