import pytest
from mrwhisker.main import render


def test_render_string():
    assert render("I'm Mr. Whisker") == "I'm Mr. Whisker"


def test_render_html():
    with open("tests/test.html") as html:
        assert render(html) == "<h1>Mr. Whisker</h1>"


def test_raise_error_template_not_string_or_file():
    with pytest.raises(TypeError) as e:
        render(123)
    assert str(e.value) == "Template must be a string or file object"
