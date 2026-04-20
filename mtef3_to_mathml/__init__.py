import logging
import struct
from dataclasses import dataclass
from io import BytesIO
from pathlib import Path

import olefile
from lxml import etree

from mtef3_to_mathml.char_replacer import replace
from mtef3_to_mathml.mover import move

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

TRANSFORM_XSL_PATH = Path(__file__).parent / "transform.xsl"
MATHML_XSLT = etree.XSLT(etree.parse(str(TRANSFORM_XSL_PATH)))

TMPL_DEFS = (
    ("tmANGLE", ("tvBANGLE", "tvLANGLE", "tvRANGLE")),
    ("tmPAREN", ("tvBPAREN", "tvLPAREN", "tvRPAREN")),
    ("tmBRACE", ("tvBBRACE", "tvLBRACE", "tvRBRACE")),
    ("tmBRACK", ("tvBBRACK", "tvLBRACK", "tvRBRACK")),
    ("tmBAR", ("tvBBAR", "tvLBAR", "tvRBAR")),
    ("tmDBAR", ("tvBDBAR", "tvLDBAR", "tvRDBAR")),
    ("tmFLOOR", ()),
    ("tmCEILING", ()),
    ("tmLBLB", ()),
    ("tmRBRB", ()),
    ("tmRBLB", ()),
    ("tmLBRP", ()),
    ("tmLPRB", ()),
    ("tmROOT", ("tvSQROOT", "tvNTHROOT")),
    ("tmFRACT", ("tvFFRACT", "tvPFRACT")),
    ("tmSCRIPT", ("tvSUPER", "tvSUB", "tvSUBSUP")),
    ("tmUBAR", ("tvSUBAR", "tvDUBAR")),
    ("tmOBAR", ("tvSOBAR", "tvDOBAR")),
    ("tmLARROW", ("tvLTARROW", "tvLBARROW")),
    ("tmRARROW", ("tvRTARROW", "tvRBARROW")),
    ("tmBARROW", ("tvBTARROW", "tvBBARROW")),
    ("tmSINT", ("tvNSINT", "tvLSINT", "tvBSINT", "tvNCINT", "tvLCINT")),
    ("tmDINT", ("tvNDINT", "tvLDINT", "tvNAINT", "tvLAINT")),
    ("tmTINT", ("tvNTINT", "tvLTINT", "tvNVINT", "tvLVINT")),
    ("tmSSINT", ("tvBSSINT", "tvLSSINT", "tvLCSINT")),
    ("tmDSINT", ("tvLASINT", "tvLDSINT")),
    ("tmTSINT", ("tvLVSINT", "tvLTSINT")),
    ("tmUHBRACE", ()),
    ("tmLHBRACE", ()),
    ("tmSUM", ("tvLSUM", "tvBSUM", "tvNSUM")),
    ("tmISUM", ("tvLISUM", "tvBISUM")),
    ("tmPROD", ("tvLPROD", "tvBPROD", "tvNPROD")),
    ("tmIPROD", ("tvLIPROD", "tvBIPROD")),
    ("tmCOPROD", ("tvLCOPROD", "tvBCOPROD", "tvNCOPROD")),
    ("tmICOPROD", ("tvLICOPROD", "tvBICOPROD")),
    ("tmUNION", ("tvLUNION", "tvBUNION", "tvNUNION")),
    ("tmIUNION", ("tvLIUNION", "tvBIUNION")),
    ("tmINTER", ("tvLINTER", "tvBINTER", "tvNINTER")),
    ("tmIINTER", ("tvLIINTER", "tvBIINTER")),
    ("tmLIM", ("tvULIM", "tvLLIM", "tvBLIM")),
    ("tmLDIV", ("tvLDIVW", "tvLDIVWO")),
    ("tmSLFRACT", ("tvSLFNORM", "tvSLFBASE", "tvSLFSUB")),
    ("tmINTOP", ("tvUINTOP", "tvLINTOP", "tvBINTOP")),
    ("tmSUMOP", ("tvUSUMOP", "tvLSUMOP", "tvBSUMOP")),
    ("tmLSCRIPT", ("tvLSUPER", "tvLSUB", "tvLSUBSUP")),
    ("tmDIRAC", ("tvBDIRAC", "tvLDIRAC", "tvRDIRAC")),
    ("tmUARROW", ("tvLUARROW", "tvRUARROW", "tvDUARROW")),
    ("tmOARROW", ("tvLOARROW", "tvROARROW", "tvDOARROW")),
    ("tmOARC", ()),
)

TYPEFACE = {
    1: "fnTEXT",
    2: "fnFUNCTION",
    3: "fnVARIABLE",
    4: "fnLCGREEK",
    5: "fnUCGREEK",
    6: "fnSYMBOL",
    7: "fnVECTOR",
    8: "fnNUMBER",
    9: "fnUSER1",
    10: "fnUSER2",
    11: "fnMTEXTRA",
    12: "fnTEXT_FE",
    24: "fnSPACE",
}

EMBELLISHMENT_TYPES = {
    2: "embDOT",  # single dot
    3: "embDDOT",  # double dot
    4: "embTDOT",  # triple dot
    5: "embPRIME",  # single prime
    6: "embDPRIME",  # double prime
    7: "embBPRIME",  # backwards prime (left of character)
    8: "embTILDE",  # tilde
    9: "embHAT",  # hat (circumflex)
    10: "embNOT",  # diagonal slash through character
    11: "embRARROW",  # right arrow
    12: "embLARROW",  # left arrow
    13: "embBARROW",  # double-headed arrow
    14: "embR1ARROW",  # right single-barbed arrow
    15: "embL1ARROW",  # left single-barbed arrow
    16: "embMBAR",  # mid-height horizontal bar
    17: "embOBAR",  # over-bar
    18: "embTPRIME",  # triple prime
    19: "embFROWN",  # over-arc, concave downward
    20: "embSMILE",  # over-arc, concave upward
}


LOGICAL_SIZES = {
    0: "szFULL",  # full
    1: "szSUB",  # subscript
    2: "szSUB2",  # sub-subscript
    3: "szSYM",  # symbol
    4: "szSUBSYM",  # sub-symbol
    5: "szUSER1",  # user 1
    6: "szUSER2",  # user 2
}


HALIGN_TYPES = {
    1: "left",
    2: "center",
    3: "right",
    4: "relational",  # relational operator alignment
    5: "decimal",  # decimal point alignment
}

VALIGN_TYPES = {
    0: "top_baseline",  # alignment with baseline of top line
    1: "center_baseline",  # alignment with baseline of center line
    2: "bottom_baseline",  # alignment with baseline of bottom line
    3: "center",  # vertical centering
}


PARTITION_LINE_TYPES = {0: "none", 1: "solid", 2: "dashed", 3: "dotted"}

TAB_STOP_TYPES = {0: "left", 1: "center", 2: "right", 3: "equal", 4: "decimal"}


@dataclass
class MTEF3Equation:
    records: list[dict]
    mtef_version: int
    platform: int
    product: int
    version: int
    subversion: int


def _get_mtef_ole(ole_path):
    if not olefile.isOleFile(ole_path):
        return []

    equations = []
    with olefile.OleFileIO(ole_path) as ole:
        # Word stores embedded OLE objects in the ObjectPool
        for entry in ole.listdir():
            # if 'ObjectPool' in entry[0]:
            # Look for the specific stream containing the MTEF data
            if "Equation Native" in entry[-1]:
                stream_path = "/".join(entry)
                stream = ole.openstream(stream_path)
                equations.append(stream.read())

    return equations


def _read_nudge(stream):
    dx_byte, dy_byte = stream.read(2)
    if dx_byte == 128 and dy_byte == 128:
        # Read two 16-bit signed integers (4 bytes total)
        dx, dy = struct.unpack("<hh", stream.read(4))
        return dx, dy
    else:
        # Subtract the 128 bias
        return dx_byte - 128, dy_byte - 128


def _parse_object_list(stream):
    objects = []
    logger.debug("Parsing object list")
    while True:
        record = _parse_record(stream)
        if record:
            logger.debug("Record type: %s", record["type"])
        if record is None or record["type"] == "END":
            break
        objects.append(record)
    return objects


def _parse_line(stream, options):
    xf_lspace = 0x4
    xf_ruler = 0x02
    line_data = {
        "type": "LINE",
        "line_spacing": None,
        "ruler": None,
        "subobjects": [],
    }

    # 1. Check for xfNULL (Empty placeholder line)
    # If the line is a placeholder, it has no objects and NO END RECORD.
    if options & 0x1:
        return line_data

    # 2. Check for xfLSPACE (Line spacing)
    if options & xf_lspace == xf_lspace:
        # Read 2 bytes, little-endian unsigned short
        line_spacing_bytes = stream.read(2)
        line_data["line_spacing"] = struct.unpack("<H", line_spacing_bytes)[0]

    # 3. Check for xfRULER (Ruler record follows)
    if options & xf_ruler == xf_ruler:
        # If this flag is set, the immediately following record is a RULER.
        # We parse it and store it in the line_data.
        line_data["ruler"] = _parse_record(stream)

    # 4. Parse the Object List
    # Now parse the actual mathematical contents of the line until the END
    # record
    line_data["subobjects"] = _parse_object_list(stream)

    return line_data


def _parse_ruler(stream, options):
    ruler_data = {"type": "RULER", "tab_stops": []}

    # 1. Read the number of tab stops (1 byte)
    n_stops_byte = stream.read(1)
    if not n_stops_byte:
        return ruler_data

    n_stops = n_stops_byte[0]

    # 2. Loop through and parse each tab stop
    for _ in range(n_stops):
        # Read the type (1 byte)
        tab_type = stream.read(1)[0]

        # Read the offset (2 bytes, little-endian unsigned short)
        offset = struct.unpack("<H", stream.read(2))[0]

        ruler_data["tab_stops"].append(
            {
                "tab_type_id": tab_type,
                "tab_type": TAB_STOP_TYPES.get(tab_type, "unknown"),
                "offset": offset,
            }
        )

    return ruler_data


def _parse_char(stream, options):
    xf_auto = 0x1  # function recognition candidate
    xf_embell = 0x2  # embellishment list follows
    char_data = {
        "type": "CHAR",
        "typeface": None,
        "mtcode": None,
        "is_func_start": bool(options & xf_auto),
        "embellishments": [],
        "variation": None,
    }

    # Typeface is stored biased by 128.
    # Positive result (1-12) = named typeface; negative = explicit FONT
    # record index.
    tf_byte = stream.read(1)[0]
    unbiased_typeface = tf_byte - 128
    char_data["typeface"] = unbiased_typeface

    if unbiased_typeface > 0:
        char_data["typeface"] = TYPEFACE.get(
            unbiased_typeface, f"UNKNOWN_STYLE_{unbiased_typeface}"
        )
    else:
        char_data["typeface"] = "EXPLICIT"
        char_data["explicit_font_id"] = abs(unbiased_typeface)

    # 16-bit Unicode character (little-endian)
    mtcode = struct.unpack("<H", stream.read(2))[0]

    char_data["mtcode"] = mtcode
    char_data["variation"] = (
        "textmode" if unbiased_typeface in (1, 9, 10, 24) else "mathmode"
    )

    # When xfEMBELL is set, a sequence of EMBELL records follows, terminated
    # by END
    if options & xf_embell:
        while True:
            record = _parse_record(stream)
            if record is None or record["type"] == "END":
                break
            if record["type_id"] == 6:  # RecordType.EMBELL
                char_data["embellishments"].append(record)

    return char_data


def _parse_tmpl(stream, options):
    tmpl_data = {
        "type": "TMPL",
        "selector": None,
        "variation": None,
        "tmpl_options": None,
        "subobjects": [],
    }

    # 1. Read the selector (1 byte)
    tmpl_selector = stream.read(1)[0]
    logger.debug("TMPL selector: %d", tmpl_selector)
    selector_name, variation_names = TMPL_DEFS[tmpl_selector]
    tmpl_data["selector"] = selector_name

    # 2. Read the variation (1 byte)
    variation = stream.read(1)[0]
    tmpl_data["variation"] = (
        variation_names[variation] if variation_names else None
    )

    # 3. Read the template-specific options (1 byte)
    # THIS ALWAYS EXISTS, even if it's just 0x00 for non-fences/integrals
    tmpl_data["tmpl_options"] = stream.read(1)[0]

    # 4. Parse the Subobject List (until END)
    tmpl_data["subobjects"] = _parse_object_list(stream)

    return tmpl_data


def _parse_pile(stream, options):
    xf_ruler = 0x02
    pile_data = {
        "type": "PILE",
        "halign": None,
        "valign": None,
        "ruler": None,
        "subobjects": [],
    }

    pile_data["halign"] = HALIGN_TYPES.get(stream.read(1)[0])
    pile_data["valign"] = VALIGN_TYPES.get(stream.read(1)[0])

    if options & xf_ruler == xf_ruler:
        pile_data["ruler"] = _parse_record(stream)

    pile_data["subobjects"] = _parse_object_list(stream)

    return pile_data


def _unpack_partitions(raw_bytes, num_partitions):
    """Unpacks an array of bytes into a list of 2-bit string names."""
    partitions = []

    for i in range(num_partitions):
        # 1. Which byte is this partition in? (4 partitions per byte)
        byte_idx = i // 4

        # 2. How many bits do we shift right? (0, 2, 4, or 6)
        bit_shift = (i % 4) * 2

        # 3. Extract the byte, shift it, and mask out everything except the
        # bottom 2 bits
        val = (raw_bytes[byte_idx] >> bit_shift) & 0x03

        # 4. Map the integer (0-3) to its name and append it
        partitions.append(PARTITION_LINE_TYPES.get(val, "unknown"))

    return partitions


def _parse_matrix(stream, options):
    matrix_data = {
        "type": "MATRIX",
        "valign": None,
        "h_just": None,
        "v_just": None,
        "rows": None,
        "cols": None,
        "row_parts": None,
        "col_parts": None,
        "subobjects": [],
    }

    # These are strictly 1 byte each; values are the same enums as PILE
    matrix_data["valign"] = VALIGN_TYPES.get(stream.read(1)[0])
    matrix_data["h_just"] = HALIGN_TYPES.get(stream.read(1)[0])
    matrix_data["v_just"] = VALIGN_TYPES.get(stream.read(1)[0])

    rows = stream.read(1)[0]
    cols = stream.read(1)[0]
    matrix_data["rows"] = rows
    matrix_data["cols"] = cols

    # Calculate how many bytes to read for row and column partitions
    # 2 bits per partition line, there are (rows + 1) partition lines.
    # + 7 to force rounding up to the nearest byte
    row_bytes_to_read = ((rows + 1) * 2 + 7) // 8
    col_bytes_to_read = ((cols + 1) * 2 + 7) // 8

    num_row_parts = rows + 1
    num_col_parts = cols + 1

    # Read the raw partition bytes
    matrix_data["row_parts"] = _unpack_partitions(
        stream.read(row_bytes_to_read), num_row_parts
    )
    matrix_data["col_parts"] = _unpack_partitions(
        stream.read(col_bytes_to_read), num_col_parts
    )

    # Parse the objects (one for each element of the matrix)
    matrix_data["subobjects"] = _parse_object_list(stream)

    return matrix_data


def _parse_embell(stream, options):
    embell_val = stream.read(1)[0]

    return {
        "type": "EMBELL",
        "embell": EMBELLISHMENT_TYPES.get(embell_val, "UNKNOWN"),
    }


def _parse_font(stream, options):
    font_data = {"type": "FONT", "tface": None, "style": None, "name": None}

    # 1. Read typeface number (1 byte)
    # negative of the typeface value (unbiased) that appears in CHAR records
    # that might follow a given FONT record
    # For example, a 3 in the FONT record corresponds to 125 (-3 + 128) in the
    # CHAR record.
    font_data["tface"] = TYPEFACE[stream.read(1)[0]]

    # 2. Read style flags (1 byte)
    # 0 = normal, 1 = italic, 2 = bold, 3 = bold + italic
    font_data["style"] = stream.read(1)[0]

    # 3. Read font name (null-terminated string)
    name_bytes = bytearray()
    while True:
        char_byte = stream.read(1)
        # Break if we hit the end of the stream or the null terminator (0x00)
        if not char_byte or char_byte[0] == 0:
            break
        name_bytes.append(char_byte[0])

    # Decode the bytes into a Python string
    # ASCII is usually sufficient for these legacy font names
    font_data["name"] = name_bytes.decode("ascii", errors="ignore")

    return font_data


def _parse_size(stream, options):
    first = stream.read(1)[0]

    if first == 101:  # explicit point size
        return {
            "type": "SIZE",
            "lsize": None,
            "point_size": struct.unpack("<H", stream.read(2))[0],
            "dsize": 0,
        }
    elif first == 100:  # large delta
        lsize = stream.read(1)[0]
        dsize = struct.unpack("<h", stream.read(2))[0]  # signed
    else:  # small delta, first byte IS lsize
        lsize = first
        dsize = stream.read(1)[0] - 128

    lsize_name = LOGICAL_SIZES.get(lsize, "UNKNOWN")

    return {"type": "SIZE", "lsize": lsize_name, "dsize": dsize}


def _parse_record(stream):
    # 1. Read the tag byte
    tag_bytes = stream.read(1)
    if not tag_bytes:
        return None  # End of stream

    tag = tag_bytes[0]

    # 2. Bit mask the record type and options
    record_type = tag & 0x0F
    options = (tag & 0xF0) >> 4

    record_data = {"type_id": record_type, "options": options, "nudge": None}

    # 3. Handle nudges globally if the xfLMOVE flag (0x8) is set
    if options & 0x8:
        record_data["nudge"] = _read_nudge(stream)

    logger.debug("Record type: %d", record_type)

    # 4. Dispatch to specialized parsing functions
    if record_type == 0:
        record_data["type"] = "END"
        return record_data
    elif record_type == 1:
        record_data.update(_parse_line(stream, options))
    elif record_type == 2:
        record_data.update(_parse_char(stream, options))
    elif record_type == 3:
        record_data.update(_parse_tmpl(stream, options))
    elif record_type == 4:
        record_data.update(_parse_pile(stream, options))
    elif record_type == 5:
        record_data.update(_parse_matrix(stream, options))
    elif record_type == 6:
        record_data.update(_parse_embell(stream, options))
    elif record_type == 7:
        record_data.update(_parse_ruler(stream, options))
    elif record_type == 8:
        # might want to maintain a global font_table dictionary at the top
        # level store these as they come in
        record_data.update(_parse_font(stream, options))
    elif record_type == 9:
        record_data.update(_parse_size(stream, options))
    elif 10 <= record_type <= 14:
        # Shortcut for size records
        record_data["type"] = "SIZE"
        record_data["lsize"] = LOGICAL_SIZES.get(record_type - 10, "UNKNOWN")
        record_data["dsize"] = 0
    else:
        raise ValueError(f"Unknown record type: {record_type}")

    return record_data


TYPESIZE_TAGS = ("full", "sub", "sub2", "sym", "subsym")

RECORD_TAGS = {
    "LINE": "slot",
    "CHAR": "char",
    "TMPL": "tmpl",
    "PILE": "pile",
    "MATRIX": "matrix",
    "EMBELL": "embell",
    "RULER": "ruler",
    "FONT": "font",
    "SIZE": "size",
}

# These fields contain nested records and are handled explicitly
_RECORD_FIELDS = {"subobjects", "embellishments", "ruler", "tab_stops"}
# These are parse-level bookkeeping that don't belong in the XML
_SKIP_FIELDS = {"type", "type_id", "options"}

_XML_KEY_MAP = {"mtcode": "mt_code_value"}
_XML_CHAR_MAP = {
    0xEB04: 0xA0,
    0xEB03: 0xA0,
    0xEB02: 0xA0,
}
_XML_TYPEFACE_MAP = {v: str(k) for k, v in TYPEFACE.items()}


def _build_xml(record):
    type_id = record.get("type_id")
    rec_type = record.get("type")

    # TYPESIZE shortcut records (type_id 10-14 → full/sub/sub2/sym/subsym)
    if type_id is not None and 10 <= type_id <= 14:
        return etree.Element(TYPESIZE_TAGS[type_id - 10])

    tag = RECORD_TAGS.get(
        rec_type, rec_type.lower() if rec_type else "unknown"
    )
    elem = etree.Element(tag)

    for key, val in record.items():
        if key in _SKIP_FIELDS or key in _RECORD_FIELDS or val is None:
            continue

        if key == "mtcode":
            val = _XML_CHAR_MAP.get(val, val)
            val = f"0x{val:04X}"
        elif key == "typeface":
            val = _XML_TYPEFACE_MAP.get(val, val)
        xml_key = _XML_KEY_MAP.get(key, key)

        if isinstance(val, list):
            # e.g. variation flags — emit one element per item
            for item in val:
                child = etree.SubElement(elem, xml_key)
                child.text = str(item)
        elif isinstance(val, tuple):
            # e.g. nudge (dx, dy)
            child = etree.SubElement(elem, xml_key)
            child.text = str(val)
        else:
            child = etree.SubElement(elem, xml_key)
            child.text = str(val)

    # Ruler is a single nested record
    ruler = record.get("ruler")
    if ruler and ruler.get("type") != "END":
        elem.append(_build_xml(ruler))

    # Embellishments are a list of EMBELL records on a CHAR
    for emb in record.get("embellishments", []):
        elem.append(_build_xml(emb))

    # Tab stops are plain dicts inside RULER records
    for stop in record.get("tab_stops", []):
        stop_elem = etree.SubElement(elem, "tab_stop")
        for k, v in stop.items():
            sc = etree.SubElement(stop_elem, k)
            sc.text = str(v)

    # Recurse into subobjects
    for sub in record.get("subobjects", []):
        if sub.get("type") != "END":
            elem.append(_build_xml(sub))

    return elem


def build_mtef_xml(equation: MTEF3Equation):
    root = etree.Element("mtef")
    for record in equation.records:
        if record.get("type") != "END":
            root.append(_build_xml(record))
    comment = etree.Comment(
        f"MTEF Version: {equation.mtef_version}, "
        f"Platform: {equation.platform}, "
        f"Product: {equation.product}, "
        f"Version: {equation.version}, "
        f"Subversion: {equation.subversion}"
    )
    root.append(comment)
    return root


def _parse_equation_stream(stream):
    mtef_version, platform, product, version, subversion = struct.unpack(
        "5B", stream.read(5)
    )

    if mtef_version != 3:
        raise ValueError(f'Expected MTEF version 3, got: "{mtef_version}"')

    logger.debug(
        "MTEF Version: %d\t"
        "Platform: %d\t"
        "Product: %d\t"
        "Version: %d\t"
        "Subversion: %d",
        mtef_version,
        platform,
        product,
        version,
        subversion,
    )

    records = []
    while True:
        record = _parse_record(stream)
        if record is None:
            break
        records.append(record)

    return MTEF3Equation(
        records, mtef_version, platform, product, version, subversion
    )


def iter_parse_equations(p: Path, raise_on_error=True):
    for equation in _get_mtef_ole(p):
        offset = equation[0]
        with BytesIO(equation[offset:]) as stream:
            try:
                yield _parse_equation_stream(stream)
            except Exception as e:
                if raise_on_error:
                    raise
                logger.exception(e)
                yield None


def parse_equations(p: Path, raise_on_error=True):
    return list(iter_parse_equations(p, raise_on_error))


def _slurp_numbers(nodes):
    mn_tag = "mn"
    mo_tag = "mo"

    for parent in nodes:
        i = 0
        while i + 2 < len(parent):
            if (
                parent[i].tag == mn_tag
                and parent[i + 1].tag == mo_tag
                and (parent[i + 1].text or "").strip() == "."
                and parent[i + 2].tag == mn_tag
            ):
                parent[i].text = (
                    (parent[i].text or "") + "." + (parent[i + 2].text or "")
                )
                parent[i].tail = parent[i + 2].tail
                parent.remove(parent[i + 2])
                parent.remove(parent[i + 1])
                # don't increment — merged element might be followed by another .<mn>
            else:
                i += 1


def transform_mathml(tree: etree._Element, block=False, raise_on_error=True):
    try:
        el = etree.Element("equation_options")
        el.text = "block" if block else "inline"
        tree.insert(0, el)
        move(tree)
        replace(tree)
        xslt_result = MATHML_XSLT(tree)
        root = xslt_result.getroot()
        _slurp_numbers(list(root.iter()))
        return root
    except Exception as e:
        if raise_on_error:
            raise
        logger.exception(e)
        return None
