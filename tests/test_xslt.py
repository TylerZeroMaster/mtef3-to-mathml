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
    """tmROOT/tvSQROOT → <msqrt>."""
    return serialize(MATHML_XSLT(inline("""
      <tmpl>
        <selector>tmROOT</selector>
        <variation>tvSQROOT</variation>
        <tmpl_options>0</tmpl_options>
        <slot><mi>x</mi></slot>
      </tmpl>""")))
