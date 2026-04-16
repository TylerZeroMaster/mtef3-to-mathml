import sys
from pathlib import Path
import json

from lxml import etree

from mtef3_to_mathml import (
    build_mtef_xml,
    iter_parse_equations,
    transform_mathml,
)

def main():
    p = Path(sys.argv[1])

    equations = iter_parse_equations(p)
    ast = (build_mtef_xml(eq) for eq in equations if eq is not None)
    mathml = (transform_mathml(mtef_xml) for mtef_xml in ast)
    dumps = json.dumps(
        [etree.tostring(m, pretty_print=True, encoding="unicode")
         for m in mathml],
        ensure_ascii=False,
        indent=2
    )
    print(dumps)


if __name__ == "__main__":
    main()
