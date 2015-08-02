import contoml
from contoml.elements import traversal as t, factory as element_factory
from contoml.prettifier import linelength


def test_linelength():
    toml_text = """
k = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. In et lectus nec erat condimentum scelerisque gravida sed ipsum. Mauris non orci tincidunt, viverra enim eget, tincidunt orci. Sed placerat nibh vitae ante maximus egestas maximus eu quam. Praesent vehicula mauris vestibulum, mattis turpis sollicitudin, aliquam felis. Pellentesque volutpat pharetra purus vel finibus. Vestibulum sed tempus dui. Maecenas auctor sit amet diam et porta. Morbi id libero at elit ultricies porta vel vitae nullam. "
"""

    expected_toml_text = """
k = \"\"\"
Lorem ipsum dolor sit amet, consectetur adipiscing elit. In et lectus nec erat condimentum scelerisque gravida sed \\
ipsum. Mauris non orci tincidunt, viverra enim eget, tincidunt orci. Sed placerat nibh vitae ante maximus egestas \\
maximus eu quam. Praesent vehicula mauris vestibulum, mattis turpis sollicitudin, aliquam felis. Pellentesque volutpat \\
pharetra purus vel finibus. Vestibulum sed tempus dui. Maecenas auctor sit amet diam et porta. Morbi id libero at elit \\
ultricies porta vel vitae nullam. \"\"\"
"""
    f = contoml.loads(toml_text)
    f.prettify(prettifiers=[linelength.line_lingth_limiter])

    assert expected_toml_text == f.dumps()
