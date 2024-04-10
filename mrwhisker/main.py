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
    token_stack = [token for token in tokenize(template)]
    while token_stack:
        token = token_stack.pop()
        template = eval_template(template, token, data)

    return template


# TOKEN_MATCHER = r'({{2,3}\s*.*?\s*}{2,3})'
TOKEN_MATCHER = r'({{2,3}\s*\S*?\s*}{2,3})'


VARIABLE_TOKEN_MATCHER = r'{{\s*(\w+)\s*}}'
# RAW_HTML_TOKEN_MATCHER = r'{{{\s*(\w*)\s*}}}|{{&\s*(\w*)\s*}}'


class TokenType(Enum):
    INTERPOLATION = 'variable'
    RAW_HTML = 'raw_html'
    SECTION = 'section'


class Token:
    def __init__(self, match: str, key: str,  token_type: TokenType = TokenType.INTERPOLATION):
        self.match = match
        self.key = key
        self._type = token_type


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


def get_value(key: str, data: Union[str, dict]) -> str:
    """
    Get the value of a key from the data
    Args:
    key (str): The key to get the value for
    data (str, dict): The data to get the value from
    return (str): The value of the key
    """
    if isinstance(data, str):
        return data

    dotted_keys = key.split('.')
    if len(dotted_keys) > 1:
        value = data
        for k in dotted_keys:
            # ? should an error be raised if the key is not found ?
            value = value.get(k, '')
        return value
    return data.get(key, '')


def tokenize(template: str) -> Generator[Token, None, None]:
    for match in re.finditer(TOKEN_MATCHER, template):
        token_match = match.group()
        token_var = token_match.strip('{&}')
        yield Token(match=token_match, key=token_var)


def eval_token(token: Token, data: Union[str, dict]) -> str:
    value = get_value(token.key, data)
    if not value:
        value = ''
    if isinstance(value, (int, float)):
        value = str(value)
    if is_html_escape(token.match):
        value = html.escape(value)
    return value


def eval_template(template: str, token: Token, data: Union[str, dict]) -> str:
    value = eval_token(token, data)
    return template.replace(token.match, value)
