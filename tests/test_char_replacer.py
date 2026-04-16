from lxml import etree
from pytest_verify import verify_snapshot

from mtef3_to_mathml.char_replacer import replace


def make_tree(mt_code_hex, variation="mathmode"):
    return etree.fromstring(f"""<slot>
      <char>
        <mt_code_value>{mt_code_hex}</mt_code_value>
        <variation>{variation}</variation>
      </char>
    </slot>""")


def serialize(el):
    return etree.tostring(el, pretty_print=True, encoding="unicode")


@verify_snapshot()
def test_variable_letter_mathmode():
    """Letter x (0x0078) in mathmode → <mi>x</mi>."""
    return serialize(replace(make_tree("0x0078")))


@verify_snapshot()
def test_uppercase_letter_mathmode():
    """Letter A (0x0041) in mathmode → <mi>A</mi>."""
    return serialize(replace(make_tree("0x0041")))


@verify_snapshot()
def test_digit_mathmode():
    """Digit 5 (0x0035) in mathmode → <mn>5</mn>."""
    return serialize(replace(make_tree("0x0035")))


@verify_snapshot()
def test_plus_operator():
    """Plus sign (0x002B) in mathmode → <mo>+</mo>."""
    return serialize(replace(make_tree("0x002B")))


@verify_snapshot()
def test_left_paren():
    """Left paren (0x0028) in mathmode → <mo stretchy='false'>(</mo>."""
    return serialize(replace(make_tree("0x0028")))


@verify_snapshot()
def test_letter_textmode():
    """Letter x in textmode → raw text node (char element removed)."""
    return serialize(replace(make_tree("0x0078", "textmode")))


@verify_snapshot()
def test_digit_textmode():
    """Digit in textmode → raw text (number typeface, textmode)."""
    return serialize(replace(make_tree("0x0035", "textmode")))


@verify_snapshot()
def test_unknown_code_unchanged():
    """A code not in the replacements dict leaves the char element in place."""
    # 0x0025 (%) is not in the replacements dict
    return serialize(replace(make_tree("0x0025")))


@verify_snapshot()
def test_multiple_chars():
    """Multiple chars in a slot are each replaced independently."""
    tree = etree.fromstring("""<slot>
      <char><mt_code_value>0x0078</mt_code_value><variation>mathmode</variation></char>
      <char><mt_code_value>0x002B</mt_code_value><variation>mathmode</variation></char>
      <char><mt_code_value>0x0079</mt_code_value><variation>mathmode</variation></char>
    </slot>""")
    return serialize(replace(tree))
