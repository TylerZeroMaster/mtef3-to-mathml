from pathlib import Path

import pytest
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


@verify_snapshot()
def test_desync1():
    """Stray extra END closes the top-level LINE one record early (t-prime
    equation from osbooks-college-physics-bundle); the rest of the equation
    must be reassembled instead of dropped."""
    return pipeline(FIXTURES / "DESYNC1.bin")


@verify_snapshot()
def test_desync2():
    """Same stray-END pattern, but closing a top-level PILE early: extra
    SIZE records leak out as top-level siblings instead of staying nested
    in the pile's rows (osbooks-college-physics-bundle Ch04, image104)."""
    return pipeline(FIXTURES / "DESYNC2.bin")


@verify_snapshot()
def test_desync3():
    """Same PILE-early-close pattern as test_desync2 (Ch04, image108)."""
    return pipeline(FIXTURES / "DESYNC3.bin")


def test_desync4():
    """Same PILE-early-close pattern with multiple stray rows leaking out
    (osbooks-college-physics-bundle Ch03, image37). One row (R' = sqrt of
    sum of squares, raised to the 1/2 power) has a desync inside a nested
    TMPL, one level deeper than the PILE-row repair handles -- the shape
    validator catches this and raises rather than silently emitting a
    wrong-but-plausible render."""
    with pytest.raises(ValueError, match="shape validation"):
        pipeline(FIXTURES / "DESYNC4.bin")


@verify_snapshot()
def test_desync5():
    """Single top-level LINE case again, with two embellished chars in the
    same line (R'' = B - A = -R') (osbooks-college-physics-bundle SSM
    Ch03, image20)."""
    return pipeline(FIXTURES / "DESYNC5.bin")


@verify_snapshot()
def test_desync6():
    """Same 2-row PILE-early-close pattern as test_desync3, extracted from
    a different manual for the same underlying equation (SSM Ch04,
    image57)."""
    return pipeline(FIXTURES / "DESYNC6.bin")


@verify_snapshot()
def test_desync7():
    """Minimal single-embellishment case: a LINE containing one embellished
    CHAR followed by a fraction TMPL that leaked out to the top level
    (CollegePhysics2e-ISM-Ch04, image100)."""
    return pipeline(FIXTURES / "DESYNC7.bin")

