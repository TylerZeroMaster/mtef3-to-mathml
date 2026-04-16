from lxml import etree
from pytest_verify import verify_snapshot

from mtef3_to_mathml.mover import move


def xml(s):
    return etree.fromstring(s)


def serialize(el):
    return etree.tostring(el, pretty_print=True, encoding="unicode")


def char(mt_code):
    return f"""<char>
      <mt_code_value>{mt_code}</mt_code_value>
      <variation>mathmode</variation>
    </char>"""


@verify_snapshot()
def test_char_before_subscript():
    """Preceding char moves into a new first slot of tmSCRIPT."""
    tree = xml(f"""<slot>
      {char('0x0078')}
      <tmpl>
        <selector>tmSCRIPT</selector>
        <variation>tvSUB</variation>
        <tmpl_options>0</tmpl_options>
        <slot>{char('0x0032')}</slot>
      </tmpl>
    </slot>""")
    return serialize(move(tree))


@verify_snapshot()
def test_char_before_superscript():
    """Preceding char moves into a new first slot of tmSCRIPT/tvSUPER."""
    tree = xml(f"""<slot>
      {char('0x0078')}
      <tmpl>
        <selector>tmSCRIPT</selector>
        <variation>tvSUPER</variation>
        <tmpl_options>0</tmpl_options>
        <slot/>
        <slot>{char('0x0032')}</slot>
      </tmpl>
    </slot>""")
    return serialize(move(tree))


@verify_snapshot()
def test_tmpl_before_subscript():
    """A preceding tmpl moves into the base slot of tmSCRIPT."""
    tree = xml(f"""<slot>
      <tmpl>
        <selector>tmFRACT</selector>
        <variation>tvFFRACT</variation>
        <tmpl_options>0</tmpl_options>
        <slot><mi>a</mi></slot>
        <slot><mi>b</mi></slot>
      </tmpl>
      <tmpl>
        <selector>tmSCRIPT</selector>
        <variation>tvSUB</variation>
        <tmpl_options>0</tmpl_options>
        <slot>{char('0x0032')}</slot>
      </tmpl>
    </slot>""")
    return serialize(move(tree))


@verify_snapshot()
def test_paren_group_before_subscript():
    """A parenthesized group before tmSCRIPT moves as a unit into the base slot."""
    tree = xml(f"""<slot>
      {char('0x0028')}
      {char('0x0078')}
      {char('0x0029')}
      <tmpl>
        <selector>tmSCRIPT</selector>
        <variation>tvSUB</variation>
        <tmpl_options>0</tmpl_options>
        <slot>{char('0x0032')}</slot>
      </tmpl>
    </slot>""")
    return serialize(move(tree))


@verify_snapshot()
def test_no_preceding_sibling_unchanged():
    """tmSCRIPT with no preceding char/tmpl sibling is left unchanged."""
    tree = xml(f"""<slot>
      <tmpl>
        <selector>tmSCRIPT</selector>
        <variation>tvSUB</variation>
        <tmpl_options>0</tmpl_options>
        <slot>{char('0x0032')}</slot>
      </tmpl>
    </slot>""")
    return serialize(move(tree))


@verify_snapshot()
def test_lscript_moves_following_char():
    """tmLSCRIPT moves following char into a new first slot."""
    tree = xml(f"""<slot>
      <tmpl>
        <selector>tmLSCRIPT</selector>
        <variation>tvLSUB</variation>
        <tmpl_options>0</tmpl_options>
        <slot>{char('0x0032')}</slot>
      </tmpl>
      {char('0x0078')}
    </slot>""")
    return serialize(move(tree))


@verify_snapshot()
def test_lscript_no_following_sibling_unchanged():
    """tmLSCRIPT with no following char/tmpl sibling is left unchanged."""
    tree = xml(f"""<slot>
      <tmpl>
        <selector>tmLSCRIPT</selector>
        <variation>tvLSUB</variation>
        <tmpl_options>0</tmpl_options>
        <slot>{char('0x0032')}</slot>
      </tmpl>
    </slot>""")
    return serialize(move(tree))


@verify_snapshot()
def test_lscript_moves_paren_group():
    """tmLSCRIPT moves a following parenthesized group as a unit into the base slot."""
    tree = xml(f"""<slot>
      <tmpl>
        <selector>tmLSCRIPT</selector>
        <variation>tvLSUB</variation>
        <tmpl_options>0</tmpl_options>
        <slot>{char('0x0032')}</slot>
      </tmpl>
      {char('0x0028')}
      {char('0x0078')}
      {char('0x0029')}
    </slot>""")
    return serialize(move(tree))


@verify_snapshot()
def test_embell_inversion():
    """char containing embell gets restructured to embell wrapping char."""
    tree = xml("""<slot>
      <char>
        <mt_code_value>0x0078</mt_code_value>
        <variation>mathmode</variation>
        <embell>
          <embell>emb1DOT</embell>
        </embell>
      </char>
    </slot>""")
    return serialize(move(tree))
