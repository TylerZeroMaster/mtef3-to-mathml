import pytest
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
      {char("0x0078")}
      <tmpl>
        <selector>tmSCRIPT</selector>
        <variation>tvSUB</variation>
        <tmpl_options>0</tmpl_options>
        <slot>{char("0x0032")}</slot>
      </tmpl>
    </slot>""")
    return serialize(move(tree))


@verify_snapshot()
def test_char_before_superscript():
    """Preceding char moves into a new first slot of tmSCRIPT/tvSUPER."""
    tree = xml(f"""<slot>
      {char("0x0078")}
      <tmpl>
        <selector>tmSCRIPT</selector>
        <variation>tvSUPER</variation>
        <tmpl_options>0</tmpl_options>
        <slot/>
        <slot>{char("0x0032")}</slot>
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
        <slot>{char("0x0032")}</slot>
      </tmpl>
    </slot>""")
    return serialize(move(tree))


@verify_snapshot()
def test_paren_group_before_subscript():
    """A parenthesized group before tmSCRIPT moves as a unit into the base slot."""
    tree = xml(f"""<slot>
      {char("0x0028")}
      {char("0x0078")}
      {char("0x0029")}
      <tmpl>
        <selector>tmSCRIPT</selector>
        <variation>tvSUB</variation>
        <tmpl_options>0</tmpl_options>
        <slot>{char("0x0032")}</slot>
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
        <slot>{char("0x0032")}</slot>
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
        <slot>{char("0x0032")}</slot>
      </tmpl>
      {char("0x0078")}
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
        <slot>{char("0x0032")}</slot>
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
        <slot>{char("0x0032")}</slot>
      </tmpl>
      {char("0x0028")}
      {char("0x0078")}
      {char("0x0029")}
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


def _group_before_superscript(text):
    """Build a slot of chars spelling ``text`` followed by a tmSCRIPT
    superscript, run the mover, and return (base text, text left outside)."""
    chars = "".join(char(f"0x{ord(c):04X}") for c in text)
    tree = xml(f"""<slot>
      {chars}
      <tmpl>
        <selector>tmSCRIPT</selector>
        <variation>tvSUPER</variation>
        <tmpl_options>0</tmpl_options>
        <slot/>
        <slot>{char("0x0032")}</slot>
      </tmpl>
    </slot>""")
    move(tree)

    def spell(parent):
        return "".join(
            chr(int(c.findtext("mt_code_value"), 16))
            for c in parent
            if c.tag == "char"
        )

    base_slot = tree.find("tmpl").findall("slot")[0]
    return spell(base_slot), spell(tree)


def test_plain_group_is_the_superscript_base():
    assert _group_before_superscript("(a+b)") == ("(a+b)", "")


def test_only_the_group_is_taken_after_a_coefficient():
    assert _group_before_superscript("x(a+b)") == ("(a+b)", "x")


def test_nested_group_is_taken_whole():
    """(4(0)+8)^2 -- the base used to be only the inner (0)."""
    assert _group_before_superscript("(4(0)+8)") == ("(4(0)+8)", "")


def test_nested_group_at_the_front_is_taken_whole():
    assert _group_before_superscript("((a)-6)") == ("((a)-6)", "")


def test_mixed_bracket_types_match_by_type():
    assert _group_before_superscript("[a(b)]") == ("[a(b)]", "")


def test_group_after_other_terms_leaves_them_outside():
    assert _group_before_superscript("7-(4(0)+8)") == ("(4(0)+8)", "7-")


def test_unmatched_closing_fence_moves_nothing():
    """No opening fence among the siblings: same as before (empty base)."""
    assert _group_before_superscript("a+b)") == ("", "a+b)")


# ---------------------------------------------------------------------------
# Scripts after groups that contain earlier scripts. Same cases as the Ruby
# converter's tests (super-ancillary-generator tests/test_mover_rb.py): a
# spec like "(8a^{3})^{2}" is built into a slot of chars and tmSCRIPT
# templates, run through the mover, and compared as a compact string with
# each script shown as SUP<base> / SUB<base>.
# ---------------------------------------------------------------------------


def _spec_tree(spec):
    parts = []
    i = 0
    while i < len(spec):
        if spec[i] in "^_" and spec[i + 1] == "{":
            end = spec.index("}", i)
            body = "".join(char(f"0x{ord(c):04X}") for c in spec[i + 2 : end])
            if spec[i] == "^":
                parts.append(f"""<tmpl>
                  <selector>tmSCRIPT</selector>
                  <variation>tvSUPER</variation>
                  <tmpl_options>0</tmpl_options>
                  <slot/>
                  <slot>{body}</slot>
                </tmpl>""")
            else:
                parts.append(f"""<tmpl>
                  <selector>tmSCRIPT</selector>
                  <variation>tvSUB</variation>
                  <tmpl_options>0</tmpl_options>
                  <slot>{body}</slot>
                </tmpl>""")
            i = end + 1
        else:
            parts.append(char(f"0x{ord(spec[i]):04X}"))
            i += 1
    return xml("<slot>" + "".join(parts) + "</slot>")


def _render(parent):
    out = []
    for node in parent:
        if node.tag == "char":
            out.append(chr(int(node.findtext("mt_code_value"), 16)))
        elif node.tag == "tmpl":
            tag = "SUP" if node.findtext("variation") == "tvSUPER" else "SUB"
            out.append(f"{tag}<{_render(node.find('slot'))}>")
    return "".join(out)


def _moved(spec):
    return _render(move(_spec_tree(spec)))


@pytest.mark.parametrize(
    ("spec", "expected"),
    [
        pytest.param("x^{2}", "SUP<x>", id="single-char-base"),
        pytest.param("(a+b)^{2}", "SUP<(a+b)>", id="plain-group"),
        pytest.param("x(a+b)^{2}", "xSUP<(a+b)>", id="coefficient-stays"),
        pytest.param("(a+b)_{1}", "SUB<(a+b)>", id="subscript-group"),
        pytest.param("x_{1}^{2}", "SUP<SUB<x>>", id="sub-then-sup"),
        pytest.param("(a)^{2}(b)^{3}", "SUP<(a)>SUP<(b)>", id="two-groups"),
        pytest.param("(4(0)+8)^{2}", "SUP<(4(0)+8)>", id="nested-group"),
        pytest.param("[a(b)]^{2}", "SUP<[a(b)]>", id="mixed-brackets"),
        pytest.param(
            "7-(4(0)+8)^{2}", "7-SUP<(4(0)+8)>", id="nested-after-terms"
        ),
        pytest.param("a+b)^{2}", "a+b)SUP<>", id="unmatched-closing-fence"),
    ],
)
def test_spec_cases_that_already_worked(spec, expected):
    assert _moved(spec) == expected


@pytest.mark.parametrize(
    ("spec", "expected"),
    [
        pytest.param("(8a^{3})^{2}", "SUP<(8SUP<a>)>", id="script-in-group"),
        pytest.param(
            "[2(s^{2})(m)]^{h}",
            "SUP<[2(SUP<s>)(m)]>",
            id="script-in-nested-group",
        ),
        pytest.param(
            "7-(8a^{3})^{2}",
            "7-SUP<(8SUP<a>)>",
            id="script-in-group-after-terms",
        ),
        pytest.param(
            "(a^{2}+b^{3})^{4}",
            "SUP<(SUP<a>+SUP<b>)>",
            id="scripts-on-both-sides-in-group",
        ),
        pytest.param(
            "(a^{2})^{3}(b)^{4}",
            "SUP<(SUP<a>)>SUP<(b)>",
            id="script-in-group-then-another-group",
        ),
    ],
)
def test_group_containing_a_script_is_taken_whole(spec, expected):
    """The group's opening fence is before the earlier script, so the fence
    search must look at every sibling before the script, not only those
    after the previous script's position."""
    assert _moved(spec) == expected
