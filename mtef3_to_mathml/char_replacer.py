from lxml import etree

MI_CHAR = "<mi>(Char)</mi>"
MN_CHAR = "<mn>(Char)</mn>"
MO_CHAR = "<mo>(Char)</mo>"
MO_CHAR_S = '<mo stretchy="false">(Char)</mo>'
CHAR = "(Char)"
MO_HEX = "<mo>(CharHex)</mo>"
MN_HEX = "<mn>(CharHex)</mn>"
MI_HEX = "<mi>(CharHex)</mi>"
MTEXT_HEX = "<mtext>(CharHex)</mtext>"
UNSUPPORTED = "Unsupported (Char)"
DEFAULT_TEXTMODE = "<mtext>(Char)</mtext>"
DEFAULT_MATHMODE = "<mi>(Char)<mi>"


def irange(start, end):
    return range(start, end + 1)


replacements = {
    0x0021: {"mathmode": MO_CHAR},
    0x0028: {"mathmode": MO_CHAR_S},
    0x0029: {"mathmode": MO_CHAR_S},
    0x002A: {"mathmode": MO_CHAR},
    0x002B: {"mathmode": MO_CHAR},
    0x002C: {"mathmode": MO_CHAR},
    0x002D: {"mathmode": MO_CHAR},
    0x002E: {"mathmode": MO_CHAR},
    0x002F: {"mathmode": MO_CHAR},
    0x003D: {"mathmode": MO_CHAR},
    0x003F: {"mathmode": MO_CHAR},
    0x005B: {"mathmode": MO_CHAR_S},
    0x005D: {"mathmode": MO_CHAR_S},
    0x007E: {"mathmode": MO_CHAR},
    **{
        k: {"mathmode": UNSUPPORTED, "textmode": UNSUPPORTED}
        for k in irange(0x0000, 0x0008)
    },
    **{
        k: {"mathmode": UNSUPPORTED, "textmode": UNSUPPORTED}
        for k in irange(0x000B, 0x001F)
    },
    **{
        k: {"mathmode": MN_CHAR, "number": CHAR, "textmode": MN_CHAR}
        for k in irange(0x0030, 0x0039)
    },
    **{
        k: {"mathmode": MO_CHAR, "textmode": CHAR}
        for k in irange(0x003A, 0x003B)
    },
    **{
        k: {"mathmode": MI_CHAR, "textmode": CHAR}
        for k in irange(0x0041, 0x005A)
    },
    **{
        k: {"mathmode": MI_CHAR, "textmode": CHAR}
        for k in irange(0x0061, 0x007A)
    },
    **{
        k: {"mathmode": UNSUPPORTED, "textmode": UNSUPPORTED}
        for k in irange(0x0080, 0x009F)
    },
    **{k: {"mathmode": MO_HEX} for k in irange(0x00A0, 0x00B0)},
    **{k: {"mathmode": MO_HEX} for k in irange(0x00B2, 0x00BB)},
    **{k: {"mathmode": MN_HEX} for k in irange(0x00BC, 0x00BE)},
    **{k: {"mathmode": MO_HEX} for k in irange(0x02C6, 0x02FF)},
    **{k: {"mathmode": MO_HEX} for k in irange(0x0300, 0x036F)},
    **{k: {"mathmode": MTEXT_HEX} for k in irange(0x2000, 0x200B)},
    **{
        k: {"mathmode": UNSUPPORTED, "textmode": UNSUPPORTED}
        for k in irange(0x200C, 0x200F)
    },
    **{k: {"mathmode": MO_HEX} for k in irange(0x2010, 0x2027)},
    **{
        k: {"mathmode": UNSUPPORTED, "textmode": UNSUPPORTED}
        for k in irange(0x2028, 0x202F)
    },
    **{k: {"mathmode": MO_HEX} for k in irange(0x2030, 0x2069)},
    **{
        k: {"mathmode": UNSUPPORTED, "textmode": UNSUPPORTED}
        for k in irange(0x206A, 0x206F)
    },
    **{k: {"mathmode": MO_HEX} for k in irange(0x2070, 0x209F)},
    **{k: {"mathmode": MI_HEX} for k in irange(0x20A0, 0x20CF)},
    **{k: {"mathmode": MO_HEX} for k in irange(0x20D0, 0x20FF)},
    **{k: {"mathmode": MO_HEX} for k in irange(0x2100, 0x2101)},
    **{k: {"mathmode": MO_HEX} for k in irange(0x2103, 0x210A)},
    **{k: {"mathmode": MO_HEX} for k in irange(0x2116, 0x2117)},
    **{k: {"mathmode": MO_HEX} for k in irange(0x213C, 0x2146)},
    **{k: {"mathmode": MN_HEX} for k in irange(0x2150, 0x218F)},
    **{k: {"mathmode": MO_HEX} for k in irange(0x2190, 0x21FF)},
    **{k: {"mathmode": MO_HEX} for k in irange(0x2200, 0x2211)},
    **{k: {"mathmode": MO_HEX} for k in irange(0x2213, 0x221D)},
    **{k: {"mathmode": MO_HEX} for k in irange(0x221F, 0x22FF)},
    **{k: {"mathmode": MO_HEX} for k in irange(0x2300, 0x23FF)},
    **{k: {"mathmode": MO_HEX} for k in irange(0x2400, 0x243F)},
    **{k: {"mathmode": MO_HEX} for k in irange(0x2500, 0x257F)},
    **{k: {"mathmode": MO_HEX} for k in irange(0x2580, 0x259F)},
    **{k: {"mathmode": MO_HEX} for k in irange(0x25A0, 0x25FF)},
    **{k: {"mathmode": MO_HEX} for k in irange(0x2600, 0x267F)},
    **{k: {"mathmode": MO_HEX} for k in irange(0x2700, 0x27BF)},
    **{k: {"mathmode": MO_HEX} for k in irange(0x27F0, 0x27FF)},
    **{k: {"mathmode": MO_HEX} for k in irange(0x2900, 0x297F)},
    **{k: {"mathmode": MO_HEX} for k in irange(0x2980, 0x29AF)},
    **{k: {"mathmode": MO_HEX} for k in irange(0x29B1, 0x29DB)},
    **{k: {"mathmode": MO_HEX} for k in irange(0x29DD, 0x29FF)},
    **{k: {"mathmode": MO_HEX} for k in irange(0x2A00, 0x2AFF)},
    **{k: {"mathmode": MO_HEX} for k in irange(0x3000, 0x303F)},
    **{
        k: {"mathmode": UNSUPPORTED, "textmode": UNSUPPORTED}
        for k in irange(0xE000, 0xE900)
    },
    **{
        k: {"mathmode": UNSUPPORTED, "textmode": UNSUPPORTED}
        for k in irange(0xE905, 0xE90A)
    },
    **{
        k: {"mathmode": UNSUPPORTED, "textmode": UNSUPPORTED}
        for k in irange(0xE90D, 0xE921)
    },
    **{
        k: {"mathmode": UNSUPPORTED, "textmode": UNSUPPORTED}
        for k in irange(0xE926, 0xE92C)
    },
    **{
        k: {"mathmode": UNSUPPORTED, "textmode": UNSUPPORTED}
        for k in irange(0xE92E, 0xE931)
    },
    **{
        k: {"mathmode": UNSUPPORTED, "textmode": UNSUPPORTED}
        for k in irange(0xE934, 0xE939)
    },
    **{
        k: {"mathmode": UNSUPPORTED, "textmode": UNSUPPORTED}
        for k in irange(0xE93C, 0xE98E)
    },
    **{
        k: {"mathmode": UNSUPPORTED, "textmode": UNSUPPORTED}
        for k in irange(0xE990, 0xEA05)
    },
    **{
        k: {"mathmode": UNSUPPORTED, "textmode": UNSUPPORTED}
        for k in irange(0xEA08, 0xEA0A)
    },
    **{
        k: {"mathmode": UNSUPPORTED, "textmode": UNSUPPORTED}
        for k in irange(0xEA0D, 0xEA31)
    },
    **{
        k: {"mathmode": UNSUPPORTED, "textmode": UNSUPPORTED}
        for k in irange(0xEA36, 0xEA39)
    },
    **{
        k: {"mathmode": UNSUPPORTED, "textmode": UNSUPPORTED}
        for k in irange(0xEA3C, 0xEA3F)
    },
    **{
        k: {"mathmode": UNSUPPORTED, "textmode": UNSUPPORTED}
        for k in irange(0xEA46, 0xEB00)
    },
    **{
        k: {"mathmode": UNSUPPORTED, "textmode": UNSUPPORTED}
        for k in irange(0xEB03, 0xEB04)
    },
    **{
        k: {"mathmode": UNSUPPORTED, "textmode": UNSUPPORTED}
        for k in irange(0xEB07, 0xED09)
    },
    **{
        k: {"mathmode": UNSUPPORTED, "textmode": UNSUPPORTED}
        for k in irange(0xED14, 0xED15)
    },
    **{
        k: {"mathmode": UNSUPPORTED, "textmode": UNSUPPORTED}
        for k in irange(0xED17, 0xEE03)
    },
    **{k: {"textmode": UNSUPPORTED} for k in irange(0xEE04, 0xEE0C)},
    **{
        k: {"mathmode": UNSUPPORTED, "textmode": UNSUPPORTED}
        for k in irange(0xEE0D, 0xEE18)
    },
    **{
        k: {"mathmode": UNSUPPORTED, "textmode": UNSUPPORTED}
        for k in irange(0xEE1A, 0xEEFF)
    },
    **{
        k: {"mathmode": UNSUPPORTED, "textmode": UNSUPPORTED}
        for k in irange(0xEF09, 0xEFFF)
    },
    **{k: {"textmode": UNSUPPORTED} for k in irange(0xF000, 0xF033)},
    **{
        k: {"mathmode": UNSUPPORTED, "textmode": UNSUPPORTED}
        for k in irange(0xF034, 0xF07F)
    },
    **{k: {"textmode": UNSUPPORTED} for k in irange(0xF080, 0xF0B3)},
    **{
        k: {"mathmode": UNSUPPORTED, "textmode": UNSUPPORTED}
        for k in irange(0xF0B4, 0xF0BF)
    },
    **{k: {"textmode": UNSUPPORTED} for k in irange(0xF0C0, 0xF0C9)},
    **{
        k: {"mathmode": UNSUPPORTED, "textmode": UNSUPPORTED}
        for k in irange(0xF0CA, 0xF0FF)
    },
    **{k: {"textmode": UNSUPPORTED} for k in irange(0xF100, 0xF133)},
    **{
        k: {"mathmode": UNSUPPORTED, "textmode": UNSUPPORTED}
        for k in irange(0xF134, 0xF8FF)
    },
    **{k: {"mathmode": MTEXT_HEX} for k in irange(0xFB00, 0xFB4F)},
    **{k: {"mathmode": MO_HEX} for k in irange(0xFE35, 0xFE4F)},
}


def replacement_xml(template, mt_code):
    char_str = chr(int(mt_code, 16))
    return template.replace("(Char)", char_str).replace("(CharHex)", char_str)


def replace_character(repl, char):
    mt_code = char.findtext("mt_code_value")
    if mt_code is None:
        return
    is_textmode = char.xpath("variation = 'textmode'")
    template = repl.get(
        "textmode" if is_textmode else "mathmode",
        DEFAULT_TEXTMODE if is_textmode else DEFAULT_MATHMODE,
    )
    text = replacement_xml(template, mt_code)
    parent = char.getparent()

    if text.startswith("<"):
        new_el = etree.fromstring(text)
        char.addprevious(new_el)
    else:
        prev = char.getprevious()
        if prev is not None:
            prev.tail = (prev.tail or "") + text
        else:
            parent.text = (parent.text or "") + text
    parent.remove(char)


def replace(tree):
    for char in tree.iter("char"):
        mt_code = char.findtext("mt_code_value")
        if mt_code is None:
            continue
        repl = replacements.get(int(mt_code, 16))
        if repl is not None:
            replace_character(repl, char)
    return tree
