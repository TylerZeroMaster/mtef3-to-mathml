# mtef3-to-mathml

Converts MathType 3 equations embedded in legacy Microsoft Word `.doc` files to MathML.

## Overview

Old `.doc` files often contain equations stored as OLE-embedded `Equation Native` streams in MTEF v3 (MathType Equation Format version 3) binary format. This tool parses those streams and converts them to MathML suitable for use in web content or document processing pipelines.

Pipeline: `.doc` OLE file → extract `Equation Native` streams → parse MTEF v3 binary → XML AST → XSLT → MathML

The XSLT transformation is adapted from the [mathtype_to_mathml](https://github.com/jure/mathtype_to_mathml) Ruby gem (MIT licensed). See [NOTICE.md](NOTICE.md) for details.

## Installation

```bash
pip install mtef3-to-mathml
```

## Usage

### Command line

```bash
mtef3-to-mathml oleFile.bin
```

Outputs a JSON array of MathML strings, one per equation found in the document.

### Python API

```python
from mtef3_to_mathml import iter_parse_equations, build_mtef_xml, transform_mathml
from lxml import etree

for equation in iter_parse_equations("oleFile.bin"):
    if equation is not None:
        xml = build_mtef_xml(equation)
        mathml = transform_mathml(xml)
        print(etree.tostring(mathml, encoding="unicode"))
```

## Requirements

- Python 3.11+
- Input files must be legacy `.doc` (OLE) format — not `.docx`
