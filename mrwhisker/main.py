import re
import html
from enum import Enum
from typing import Union, List, Tuple, Generator
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
    assert isinstance(template, (str, TextIOWrapper)
                      ), "Template must be of type string or TextIOWrapper"
    assert isinstance(data, (str, dict)), "Data must be of type string or dict"

    if not data or isinstance(data, str) and data.isspace():
        data = ''

    if isinstance(template, TextIOWrapper):
        template = template.read()

    if isinstance(data, str):
        return re.sub(r'{{\s*(\w+)\s*}}', data, template)

    # * Find all the tokens in the template
    tokens = tokenize(template, data)

    for token in tokens:
        template = token.eval(template)

    return template
    # tokens, template = match_tokens(template, data)

    # if data and isinstance(data, dict):
    #     for token in tokens:
    #         # * If the token is not in the template, remove it from the template
    #         if not bool(re.search(token.key, template)):
    #             template = re.sub(token.key, '', template)
    #             continue

    #         value = token.value

    #         if token.type == TokenType.VARIABLE:
    #             value = html.escape(value, quote=False)

    #         # ! need to fix the matching here
    #         template = template.replace(token.key, value)

    # return template


# TOKEN_MATCHER = r'({{2,3}\s*.*?\s*}{2,3})'
TOKEN_MATCHER = r'({{2,3}\s*\S*?\s*}{2,3})'


# def match_tokens(template: str, data: Union[str, dict]) -> Tuple[List, str]:
#     tokens = []

#     def remove_spaces(match):
#         return match.group(1) + match.group(2).strip() + match.group(3)

#     for match in re.finditer(TOKEN_MATCHER, template):
#         token_match = match.group()
#         template = re.sub(r'({{2,3}&?)\s*(.*?)\s*(}{2,3})',
#                           remove_spaces, template)

#         token_key = re.sub(r'\s+', '', token_match)
#         # ! This feels wrong
#         unwanted_chars = "{ s* & } \\"
#         token_name = ''.join(c for c in token_key if c not in unwanted_chars)

#         if data and isinstance(data, dict):
#             value = data.get(token_name, '')

#         if not data or isinstance(data, str):
#             value = data
#         tokens.append(
#             Token(key=token_key, value=value)
#         )

#     return tokens, template


VARIABLE_TOKEN_MATCHER = r'{{\s*(\w+)\s*}}'
# RAW_HTML_TOKEN_MATCHER = r'{{{\s*(\w*)\s*}}}|{{&\s*(\w*)\s*}}'
RAW_HTML_TOKEN_MATCHER = r'{{{\s*.*\s*}}}|{{&\s*.*\s*}}'


class TokenType(Enum):
    VARIABLE = 'variable'
    RAW_HTML = 'raw_html'


# class Token:
#     def __init__(self, key: str, value: str = None):
#         self._key = key
#         self._value = value

#     def __eq__(self, other):
#         if isinstance(other, Token):
#             return self.key == other.key
#         return False

#     @property
#     def key(self):
#         return self._key

#     @property
#     def value(self):
#         return self._value if self._value else ''

#     @property
#     def type(self):
#         match self.key:
#             case str() if re.match(r'{{{\s*.*\s*}}}|{{&\s*.*\s*}}', self.key):
#                 return TokenType.RAW_HTML
#             case  str() if re.match(r'{{\s*.*\s*}}', self.key):
#                 return TokenType.VARIABLE
#             case _:
#                 raise ValueError("Invalid token type")


class Token:
    def __init__(self, key: str, value: str):
        self._key = key
        self._value = value

    def eval(self, template: str) -> str:
        return template.replace(self._key, self._value)


def tokenize(template: str, data: dict) -> Generator[Token, None, None]:
    tokens = []
    for match in re.finditer(TOKEN_MATCHER, template):
        token_match = match.group()
        token_var = token_match.strip('{}')
        token_value = data.get(token_var, '')
        # * escape html characters
        token_value = html.escape(token_value)
        tokens.append(
            Token(key=token_match, value=token_value)
        )

    for token in tokens:
        yield token
