import pytest
from tests import spec_parser
from mrwhisker.main import render

TESTS = spec_parser.parse("sections.yml")


@pytest.mark.parametrize("test_input", TESTS)
def test_sections_from_spec(test_input):
    result = render(test_input["template"], test_input["data"])
    assert result == test_input["expected"]
