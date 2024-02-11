from mrwhisker.main import render


def test_render_string():
    assert render("I'm Mr. Whisker") == "I'm Mr. Whisker"

def test_render_html():
    with open("tests/test.html") as html:
      assert render(html) == "<h1>Mr. Whisker</h1>"

