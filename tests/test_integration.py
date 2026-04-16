from pathlib import Path

from lxml import etree
from pytest_verify import verify_snapshot

from mtef3_to_mathml import build_mtef_xml, iter_parse_equations, transform_mathml

FIXTURES = Path(__file__).parent / "fixtures"


def pipeline(bin_path):
    results = []
    for eq in iter_parse_equations(bin_path, raise_on_error=True):
        if eq is None:
            continue
        mathml = transform_mathml(build_mtef_xml(eq))
        if mathml is not None:
            results.append(
                etree.tostring(mathml, pretty_print=True, encoding="unicode")
            )
    return results


@verify_snapshot()
def test_table1():
    """Multi-line equation (pile): two rows of physics working."""
    return pipeline(FIXTURES / "TABLE1.bin")


@verify_snapshot()
def test_table2():
    """Multi-line equation (pile): two rows of physics working."""
    return pipeline(FIXTURES / "TABLE2.bin")


@verify_snapshot()
def test_sub():
    """Subscript"""
    return pipeline(FIXTURES / "SUB.bin")


@verify_snapshot()
def test_subsup():
    """Subscript + superscript"""
    return pipeline(FIXTURES / "SUBSUP.bin")


@verify_snapshot()
def test_sum():
    """Summation"""
    return pipeline(FIXTURES / "SUM1.bin")

