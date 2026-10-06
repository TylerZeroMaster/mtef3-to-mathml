import copy

from lxml import etree

PARENS_SELECTOR = (
    "selector='tmPARENS' or "
    "selector='tmBRACK' or "
    "selector='tmBRACE' or "
    "selector='tmOBRACK' or "
    "selector='tmOBRACE' or "
    "selector='tmHBRACK' or "
    "selector='tmHBRACE'"
)

SUBSUP_SELECTOR = "selector='tmSCRIPT' or selector='tmLSCRIPT'"

PRE = "selector='tmLSCRIPT'"

OPEN_PAREN = (
    "mt_code_value = '0x0028' or "
    "mt_code_value = '0x005B' or "
    "mt_code_value = '0x007B'"
)

CLOSE_PAREN = (
    "mt_code_value = '0x0029' or "
    "mt_code_value = '0x005D' or "
    "mt_code_value = '0x007D'"
)

OPEN_CLOSE_PAIRS = {
    "0x0028": "0x0029",  # ( )
    "0x005B": "0x005D",  # [ ]
    "0x007B": "0x007D",  # { }
}


class Mover:
    def __init__(self, tree):
        self.tree = tree
        self.last_preceding_siblings = []
        self.all_preceding_siblings = []

    def move_until_mt_code(self, elements, mt_code_value, parent):
        for element in list(elements):
            parent.append(element)
            if element.xpath(f"mt_code_value = '{mt_code_value}'"):
                break

    def move_paren(self, siblings, node):
        for open_code, close_code in OPEN_CLOSE_PAIRS.items():
            if siblings[0].xpath(f"mt_code_value = '{open_code}'"):
                self.move_until_mt_code(siblings, close_code, node)

    def new_preceding_siblings(self, el):
        all_siblings = el.xpath(
            "preceding-sibling::tmpl | preceding-sibling::char"
        )
        last_ids = {id(s) for s in self.last_preceding_siblings}
        siblings = [s for s in all_siblings if id(s) not in last_ids]
        self.last_preceding_siblings = all_siblings
        # Kept unsubtracted for matching_fence_run: ``siblings`` drops
        # everything before the previous script's position, including the
        # opening fence of a group that contains that script.
        self.all_preceding_siblings = all_siblings
        return siblings

    def new_following_siblings(self, el):
        return el.xpath("following-sibling::tmpl | following-sibling::char")

    @staticmethod
    def matching_fence_run(siblings):
        """The trailing run of ``siblings`` from the opening fence that
        matches the final closing fence through that closing fence
        (inclusive), counting nesting depth of that fence type. Empty if no
        matching opening fence is among ``siblings``.
        """
        code = siblings[-1].find("mt_code_value")
        close_code = code.text if code is not None else None
        open_code = next(
            (o for o, c in OPEN_CLOSE_PAIRS.items() if c == close_code), None
        )
        if open_code is None:
            return []

        depth = 0
        for index, sibling in enumerate(reversed(siblings), start=1):
            code = sibling.find("mt_code_value")
            text = code.text if code is not None else None
            if text == close_code:
                depth += 1
            elif text == open_code:
                depth -= 1
            if depth == 0:
                return siblings[-index:]
        return []

    def move_following_subsup(self):
        for el in self.tree.xpath(
            f"//tmpl[({SUBSUP_SELECTOR}) and not({PRE})]"
        ):
            siblings = self.new_preceding_siblings(el)
            if not siblings:
                continue

            node = etree.Element("slot")

            if siblings[-1].xpath(CLOSE_PAREN):
                # Take the run from the opening fence that matches the final
                # closing fence. The original scan took the nearest opening
                # fence behind the script and moved elements only up to the
                # first closing fence after it -- no nesting depth -- so for
                # "(4(0)+8)^2" the base became the inner "(0)", leaving
                # "(4+8)" outside and the exponent on the wrong group.
                run = self.matching_fence_run(self.all_preceding_siblings)
                if run:
                    for s in run:
                        node.append(s)
                else:
                    # No matching opening fence before the script at all:
                    # keep the original nearest-fence scan rather than leave
                    # the base empty.
                    filtered = []
                    for s in reversed(siblings):
                        next_el = s.getnext()
                        if next_el is not None and next_el.xpath(OPEN_PAREN):
                            break
                        filtered.append(s)
                    siblings = list(reversed(filtered))
                    self.move_paren(siblings, node)
            else:
                # handles both tmpl[PARENS_SELECTOR] and plain element cases
                node.append(siblings[-1])

            first_slot = el.find("slot")
            if first_slot is not None:
                first_slot.addprevious(node)

    def move_preceding_subsup(self):
        for el in self.tree.xpath(f"//tmpl[({SUBSUP_SELECTOR}) and {PRE}]"):
            siblings = self.new_following_siblings(el)
            if not siblings:
                continue

            node = etree.Element("slot")

            if siblings[0].xpath(OPEN_PAREN):
                filtered = []
                for s in reversed(siblings):
                    next_el = s.getnext()
                    if next_el is not None and next_el.xpath(CLOSE_PAREN):
                        break
                    filtered.append(s)
                siblings = list(reversed(filtered))
                self.move_paren(siblings, node)
            else:
                node.append(siblings[0])

            first_slot = el.find("slot")
            if first_slot is not None:
                first_slot.addprevious(node)

    def invert_char_embell(self):
        for el in self.tree.xpath("//char[embell]"):
            embell = el.find("embell")
            el.remove(embell)
            char = copy.deepcopy(el)
            embell.append(char)
            el.getparent().replace(el, embell)

    def move(self):
        self.move_following_subsup()
        self.move_preceding_subsup()
        self.invert_char_embell()


def move(tree):
    Mover(tree).move()
    return tree
