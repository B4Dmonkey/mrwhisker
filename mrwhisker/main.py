import re
import html
from enum import Enum
from typing import Union
from io import TextIOWrapper


def render(template: Union[str, TextIOWrapper], data: Union[str, dict] = '') -> str:
    """
    Render a mustache template

    Args:
    template (str, TextIOWrapper): The template to render. This can be either a string or a TextIOWrapper object.
    data (str, dict): The data to use for rendering the template. This is an optional arg. This can be either a dictionary or a string.

    Returns:
    str: The rendered template.
    """
    if not isinstance(template, (str, TextIOWrapper)):
        raise TypeError("Template must be of type string or TextIOWrapper")

    if not isinstance(data, (str, dict)):
        raise TypeError("Data must be of type string or dict")

    if not data or isinstance(data, str) and data.isspace():
        data = ''

    if isinstance(template, TextIOWrapper):
        template = template.read()

    if isinstance(data, str):
        return re.sub(r'{{\s*(\w+)\s*}}', data, template)

    # * Find all the tokens in the template
    tokens = parse_tokens(template, data)

    if data and isinstance(data, dict):
        for token in tokens:
            # * If the token is not in the template, remove it from the template
            if not bool(re.search(token.key, template)):
                template = re.sub(token.key, '', template)
                continue

            value = token.value

            if token.token_type == TokenType.VARIABLE:
                value = html.escape(token.value, quote=False)

            template = re.sub(token.key, value, template)

    return template


def parse_tokens(template: str, data: Union[str, dict]) -> set:
    VARIABLE_TOKEN_MATCHER = r'{{\s*(\w+)\s*}}'
    RAW_HTML_TOKEN_MATCHER = r'{{{\s*(\w+)\s*}}}'

    tokens = []

    for match in re.finditer(RAW_HTML_TOKEN_MATCHER, template):
        FIRST_WORD = 1
        token_key = match.group(FIRST_WORD)
        tokens.append(
            Token(
                key=token_key,
                value=data.get(token_key, '') if isinstance(
                    data, dict) else data,
                token_type=TokenType.RAW_HTML
            )
        )

    for match in re.finditer(VARIABLE_TOKEN_MATCHER, template):
        FIRST_WORD = 1
        token_key = match.group(FIRST_WORD)
        tokens.append(
            Token(
                key=token_key,
                value=data.get(token_key, '') if isinstance(
                    data, dict) else data
            )
        )

    return tokens


class TokenType(Enum):
    VARIABLE = 'variable'
    RAW_HTML = 'raw_html'


class Token:
    def __init__(self, key: str, value: str = None, token_type: TokenType = TokenType.VARIABLE):
        self._key = key
        self._value = value
        self.token_type = token_type

    def __eq__(self, other):
        if isinstance(other, Token):
            return self.key == other.key
        return False

    @property
    def key(self):
        match self.token_type:
            case TokenType.VARIABLE:
                return r'{{\s*%s\s*}}' % self._key
            case TokenType.RAW_HTML:
                return r'{{{\s*%s\s*}}}' % self._key
            case _:
                raise ValueError("Invalid token type")

    @property
    def value(self):
        return self._value if self._value else ''
