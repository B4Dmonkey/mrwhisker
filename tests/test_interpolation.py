import pytest
from tests import spec_parser
from mrwhisker.main import render

TESTS = spec_parser.parse("interpolation.yml")


@pytest.mark.parametrize("spec", TESTS)
def test_interpolation_from_spec(spec):
    result = render(spec["template"], spec["data"])
    assert result == spec["expected"], spec["desc"]
