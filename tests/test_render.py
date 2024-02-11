import pytest
from mrwhisker.main import render


class TestRenderTemplate:
    def test_string(self):
        assert render("I'm Mr. Whisker") == "I'm Mr. Whisker"

    def test_file(self):
        expected = "<h1>Mr. Whisker</h1>\n<p>another mustache implementation</p>"
        with open("tests/test.html") as html:
            assert render(html) == expected

    def test_raise_error_when_template_not_string_or_file(self):
        with pytest.raises(TypeError) as e:
            render(123)
        assert str(e.value) == "Template must be of type string or TextIOWrapper"


class TestRenderData:
    def test_when_data_is_None_renders_empty_string(self):
        template = "Hello {{world}}"
        assert render(template) == "Hello "

    def test_when_data_is_empty_dict_renders_empty_string(self):
        template = "Hello {{world}}"
        assert render(template, {}) == "Hello "

    def test_when_data_is_whitespace_renders_empty_string(self):
        template = "Hello {{world}}"
        assert render(template, "\n") == "Hello "

    def test_render_variable(self):
        template = "Hello {{ var }}"
        data = "world"
        expected = "Hello world"
        assert render(template, data) == expected

    def test_render_duplicate_variables(self):
        template = "{{ v }} {{ v}} {{v}} {{v }} world"
        data = "hey"
        expected = "hey hey hey hey world"
        assert render(template, data) == expected

    def test_when_data_dict_render_variable(self):
        template = "Hello, {{ Adele }}"
        data = {"Adele": "it's me"}
        expected = "Hello, it's me"
        assert render(template, data) == expected

    def test_dict_keys_are_case_sensitive(self):
        template = "Hello, {{ Adele }}"
        data = {"adele": "it's me"}
        expected = "Hello, "
        assert render(template, data) == expected
