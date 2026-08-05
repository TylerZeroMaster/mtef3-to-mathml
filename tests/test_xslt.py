from lxml import etree
from pytest_verify import verify_snapshot

from mtef3_to_mathml import MATHML_XSLT


def xslt(xml_str):
    return etree.fromstring(xml_str)


def serialize(result):
    return etree.tostring(result, pretty_print=True, encoding="unicode")


def inline(slot_content):
    """Wrap slot content in a minimal inline mtef document."""
    return xslt(f"""<mtef>
      <equation_options>inline</equation_options>
      <slot>{slot_content}</slot>
    </mtef>""")


@verify_snapshot()
def test_inline_wrapper():
    """equation_options=inline wraps output in <math>."""
    return serialize(MATHML_XSLT(inline("<mi>x</mi>")))


@verify_snapshot()
def test_block_wrapper():
    """equation_options=block wraps output in <math display='block'>."""
    tree = xslt("""<mtef>
      <equation_options>block</equation_options>
      <slot><mi>x</mi></slot>
    </mtef>""")
    return serialize(MATHML_XSLT(tree))


@verify_snapshot()
def test_fraction():
    """tmFRACT with two slots → <mfrac>."""
    return serialize(MATHML_XSLT(inline("""
      <tmpl>
        <selector>tmFRACT</selector>
        <tmpl_options>0</tmpl_options>
        <slot><mi>a</mi></slot>
        <slot><mi>b</mi></slot>
      </tmpl>""")))


@verify_snapshot()
def test_subscript():
    """tmSCRIPT/tvSUB with base and subscript slots → <msub>."""
    return serialize(MATHML_XSLT(inline("""
      <tmpl>
        <selector>tmSCRIPT</selector>
        <variation>tvSUB</variation>
        <tmpl_options>0</tmpl_options>
        <slot><mi>x</mi></slot>
        <slot><mn>2</mn></slot>
      </tmpl>""")))


@verify_snapshot()
def test_superscript():
    """tmSCRIPT/tvSUPER with base and superscript slots → <msup>.
    slot[3] is the exponent per the XSL template."""
    return serialize(MATHML_XSLT(inline("""
      <tmpl>
        <selector>tmSCRIPT</selector>
        <variation>tvSUPER</variation>
        <tmpl_options>0</tmpl_options>
        <slot><mi>x</mi></slot>
        <slot/>
        <slot><mn>2</mn></slot>
      </tmpl>""")))


@verify_snapshot()
def test_subsup():
    """tmSCRIPT/tvSUBSUP → <msubsup>."""
    return serialize(MATHML_XSLT(inline("""
      <tmpl>
        <selector>tmSCRIPT</selector>
        <variation>tvSUBSUP</variation>
        <tmpl_options>0</tmpl_options>
        <slot><mi>x</mi></slot>
        <slot><mn>1</mn></slot>
        <slot><mn>2</mn></slot>
      </tmpl>""")))


@verify_snapshot()
def test_sqrt():
    """tmROOT/tvSQROOT with an empty index slot (slot[2], as MathType always
    emits for a plain square root) → <msqrt>, not a dropped/empty <mrow>.
    Reproduces the college-physics dropped-radical bug: tmROOT had no XSL
    template and fell through to the match="*" catch-all in transform.xsl."""
    return serialize(MATHML_XSLT(inline("""
      <tmpl>
        <selector>tmROOT</selector>
        <variation>tvSQROOT</variation>
        <tmpl_options>0</tmpl_options>
        <slot><mi>x</mi></slot>
        <slot/>
      </tmpl>""")))


@verify_snapshot()
def test_nthroot():
    """tmROOT/tvNTHROOT with radicand (slot[1]) and index (slot[2]) → <mroot>."""
    return serialize(MATHML_XSLT(inline("""
      <tmpl>
        <selector>tmROOT</selector>
        <variation>tvNTHROOT</variation>
        <tmpl_options>0</tmpl_options>
        <slot><mi>x</mi></slot>
        <slot><mn>3</mn></slot>
      </tmpl>""")))


def char(mt_code, variation):
    return f"""<char>
      <typeface>1</typeface>
      <mt_code_value>{mt_code}</mt_code_value>
      <variation>{variation}</variation>
    </char>"""


@verify_snapshot()
def test_textmode_default_greek_letter_wrapped():
    """A textmode char with no char_replacer/char.xsl override (e.g. Greek
    mu, U+03BC — not covered by char_replacer.py's replacements dict, no
    specific char.xsl template) must still land wrapped in <mtext>, not as
    bare text directly inside <mrow>. Reproduces the mtef3-to-mathml
    'bare unwrapped character' bug (college-physics SSM/ISM instances)."""
    return serialize(MATHML_XSLT(inline(char("0x03BC", "textmode"))))


@verify_snapshot()
def test_textmode_default_ascii_gap_wrapped():
    """A textmode char in one of char_replacer.py's ASCII gaps (e.g. '%',
    U+0025, which falls between the 0x0021 and 0x0028 entries) must still
    land wrapped in <mtext>, not as bare text. Reproduces the bug seen in
    college-physics ISM-Ch01 image25."""
    return serialize(MATHML_XSLT(inline(char("0x0025", "textmode"))))


@verify_snapshot()
def test_textmode_default_mathtype_pua_gap_wrapped():
    """A textmode char in the MathType private-use gap (U+EB01, uncovered
    by both char_replacer.py and char.xsl's specific templates) must still
    land wrapped in <mtext>, not as bare text."""
    return serialize(MATHML_XSLT(inline(char("0xEB01", "textmode"))))


@verify_snapshot()
def test_mathmode_default_unaffected():
    """Sanity check: the mathmode default template already wraps correctly
    (in <mi>), so an unmapped mathmode Greek letter is unaffected by the
    textmode-default bug."""
    return serialize(MATHML_XSLT(inline(char("0x03BC", "mathmode"))))


@verify_snapshot()
def test_textmode_default_char_with_embellishment_not_nested():
    """An unmapped textmode char (Greek mu) under an embellishment (dot
    accent) must land as a <mtext> SIBLING of the accent mark inside
    <mover>, not nested inside another token element. embellishment.xsl's
    `(char | mn | mo | mtext | mi)[1]` selection places whatever the char
    resolves to directly as mover's first child — guards against the
    'mtext inside mi' nesting concern raised when the textmode-default fix
    was added (char.xsl's default templates never wrap one token element
    inside another; only slot/pile/embell containers do)."""
    return serialize(MATHML_XSLT(inline(f"""
      <embell>
        <embell>embDOT</embell>
        {char("0x03BC", "textmode")}
      </embell>""")))
