from mrwhisker.main import render


class TestVariable:
    def test_render_spec_variable(self):
        with open("tests/variables/variable.html") as template:
            data = {
                "name": "Chris",
                "company": "<b>GitHub</b>",
            }
            expected = "Chris\n\n&lt;b&gt;GitHub&lt;/b&gt;\n<b>GitHub</b>"
            assert render(template, data) == expected

    def test_escapes_html(self):
        template = "Hello, {{ company }}"
        data = {
            "name": "Chris",
            "company": "<b>GitHub</b>",
        }
        expected = "Hello, &lt;b&gt;GitHub&lt;/b&gt;"
        assert render(template, data) == expected
    
    def test_when_triple_braces_does_not_escape_html(self):
        template = "Hello, {{{ company }}}"
        data = {
            "name": "Chris",
            "company": "<b>GitHub</b>",
        }
        expected = "Hello, <b>GitHub</b>"
        assert render(template, data) == expected
