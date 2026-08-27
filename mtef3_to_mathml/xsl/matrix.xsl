<?xml version="1.0" encoding="UTF-8"?>
<!--
// =====================================================
// Matrices
// =====================================================

// matrix translation (left, center, right)
matrix/l    = "<(ns)mtable columnalign='left'>$+$n#$-$n</(ns)mtable>";
matrix      = "<(ns)mtable>$+$n#$-$n</(ns)mtable>";
matrix/r    = "<(ns)mtable columnalign='right'>$+$n#$-$n</(ns)mtable>";

// matrix line translation (left, center, right)
matrow/l   = "<(ns)mtr columnalign='left'>$+$n#$-$n</(ns)mtr>$n";
matrow     = "<(ns)mtr>$+$n#$-$n</(ns)mtr>$n";
matrow/r   = "<(ns)mtr columnalign='right'>$+$n#$-$n</(ns)mtr>$n";

// matrix element translation (except for last element) (left, center, right)
matelem/l   = "<(ns)mtd columnalign='left'>$+$n#$-$n</(ns)mtd>$n";
matelem     = "<(ns)mtd>$+$n#$-$n</(ns)mtd>$n";
matelem/r   = "<(ns)mtd columnalign='right'>$+$n#$-$n</(ns)mtd>$n";

// matrix element translation (last element only) (left, center, right)
matelem/last/l   = "<(ns)mtd columnalign='left'>$+$n#$-$n</(ns)mtd>";
matelem/last     = "<(ns)mtd>$+$n#$-$n</(ns)mtd>";
matelem/last/r   = "<(ns)mtd columnalign='right'>$+$n#$-$n</(ns)mtd>";
 -->


<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    exclude-result-prefixes="xs"
    version="1.0">

    <!-- Matrices TODO -->
    <xsl:template match="matrix[h_just='left']">
        <mtable columnalign="left">
            <xsl:variable name="cols" select="number(cols)"/>
            <xsl:apply-templates select="(slot | pile)[(position() - 1) mod $cols = 0]" mode="rows-left" />
        </mtable>
    </xsl:template>

    <!-- FIX: matches whenever h_just isn't explicitly 'left' or 'right',
         not just the literal string 'center' — covers three real gaps:
         (1) h_just missing entirely, which _build_xml (mtef3_to_mathml's
         Python-to-XML step) produces whenever the parsed value is None,
         skipping the field rather than emitting e.g. <h_just/>. Confirmed
         via real production data: a 2-row/1-column matrix (a parametric
         equation system, "{x(t)=5-t, y(t)=8-2t}") had no <h_just> element
         at all — single-column matrices have no real horizontal-
         alignment concept, so this is plausibly the common case for any
         single-column matrix, not a rare edge case. (2) and (3) h_just
         values 'relational' and 'decimal' (HALIGN_TYPES has five values;
         only left/center/right had templates). All three previously fell
         through to this file's absence of any matching template, and from
         there to the base stylesheet's <xsl:template match="*" /> catch-
         all — silently dropping the entire matrix (every row/column of
         real content, not just formatting) rather than just rendering
         without a columnalign override. 'center' behavior (no columnalign
         attribute) is the correct fallback here, not a new default
         invented for this fix: it's already exactly what the upstream
         macro comment's un-suffixed "matrix" (no /l or /r) produces. -->
    <xsl:template match="matrix[not(h_just='left') and not(h_just='right')]">
        <mtable>
            <xsl:variable name="cols" select="number(cols)"/>
            <xsl:apply-templates select="(slot | pile)[(position() - 1) mod $cols = 0]" mode="rows-center" />
        </mtable>
    </xsl:template>

    <xsl:template match="matrix[h_just='right']">
        <mtable columnalign="right">
            <xsl:variable name="cols" select="number(cols)"/>
            <xsl:apply-templates select="(slot | pile)[(position() - 1) mod $cols = 0]" mode="rows-right" />
        </mtable>
    </xsl:template>

    <xsl:template match="slot | pile" mode="rows-left">
        <xsl:variable name="cols" select="number(parent::*/cols)"/>
        <mtr columnalign="left">
            <xsl:apply-templates select="." mode="columns-left" />
            <xsl:apply-templates select="(following-sibling::slot | following-sibling::pile)[position() &lt; $cols]" mode="columns-left" />
        </mtr>
    </xsl:template>

    <xsl:template match="slot | pile" mode="rows-center">
        <xsl:variable name="cols" select="number(parent::*/cols)"/>
        <mtr columnalign="center">
            <xsl:apply-templates select="." mode="columns-center" />
            <xsl:apply-templates select="(following-sibling::slot | following-sibling::pile)[position() &lt; $cols]" mode="columns-center" />
        </mtr>
    </xsl:template>

    <xsl:template match="slot | pile" mode="rows-right">
        <xsl:variable name="cols" select="number(parent::*/cols)"/>
        <mtr columnalign="right">
            <xsl:apply-templates select="." mode="columns-right" />
            <xsl:apply-templates select="(following-sibling::slot | following-sibling::pile)[position() &lt; $cols]" mode="columns-right" />
        </mtr>
    </xsl:template>

    <xsl:template match="pile" mode="columns-left">
        <mtd columnalign="left">
            <xsl:apply-templates select="."/>
        </mtd>
    </xsl:template>

    <xsl:template match="pile" mode="columns-center">
        <mtd columnalign="center">
            <xsl:apply-templates select="."/>
        </mtd>
    </xsl:template>

    <xsl:template match="pile" mode="columns-right">
        <mtd columnalign="right">
            <xsl:apply-templates select="."/>
        </mtd>
    </xsl:template>

    <xsl:template match="slot" mode="columns-left">
        <mtd columnalign="left">
            <xsl:apply-templates />
        </mtd>
    </xsl:template>

    <xsl:template match="slot" mode="columns-center">
        <mtd columnalign="center">
            <xsl:apply-templates />
        </mtd>
    </xsl:template>

    <xsl:template match="slot" mode="columns-right">
        <mtd columnalign="right">
            <xsl:apply-templates />
        </mtd>
    </xsl:template>
</xsl:stylesheet>
