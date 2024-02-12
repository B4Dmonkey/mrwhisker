from mrwhisker.main import parse_tokens, Token


class TestGetTokens:
    def test_get_tokens_from_template(self):
        template = "Hello {{world}}"
        tokens = parse_tokens(template, None)
        assert tokens == [Token("world")]
    
    def test_when_expected_token_has_white_space_gets_token(self):
        template = "Hello {{ world }}"
        tokens = parse_tokens(template, None)
        assert tokens == [Token("world")]
