<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    exclude-result-prefixes="xs"
    version="1.0">

    <!-- Fences -->
    <xsl:template match="tmpl[selector='tmPAREN']">
        <mrow>
            <mo>(</mo>
                <xsl:apply-templates select="slot[1] | pile[1]"/>
            <mo>)</mo>
        </mrow>
    </xsl:template>

    <xsl:template match="tmpl[selector='tmPAREN' and variation='tvLPAREN']">
        <mrow><mo>(</mo> <xsl:apply-templates select="slot[1] | pile[1]"/></mrow>
    </xsl:template>

    <xsl:template match="tmpl[selector='tmPAREN' and variation='tvRPAREN']">
        <mrow> <xsl:apply-templates select="slot[1] | pile[1]"/> <mo>)</mo></mrow>
    </xsl:template>

    <xsl:template match="tmpl[selector='tmBRACK']">
        <mrow>
            <mo>[</mo>
            <xsl:apply-templates select="slot[1] | pile[1]"/>
            <mo>]</mo>
        </mrow>
    </xsl:template>

    <xsl:template match="tmpl[selector='tmBRACE']">
        <mrow>
            <mo>{</mo>
            <xsl:apply-templates select="slot[1] | pile[1]"/>
            <mo>}</mo>
        </mrow>
    </xsl:template>

    <xsl:template match="tmpl[selector='tmANGLE']">
        <mrow><mo>&#x2329;</mo> <xsl:apply-templates select="slot[1] | pile[1]"/> <mo>&#x232A;</mo></mrow>
    </xsl:template>

    <xsl:template match="tmpl[selector='tmANGLE' and variation='tvLANGLE']">
        <mrow>
            <mo>&#x2329;</mo>
            <xsl:apply-templates select="slot[1] | pile[1]"/>
        </mrow>
    </xsl:template>

    <xsl:template match="tmpl[selector='tmANGLE' and variation='tvRANGLE']">
        <mrow>
            <xsl:apply-templates select="slot[1] | pile[1]"/>
            <mo>&#x232A;</mo>
        </mrow>
    </xsl:template>

    <xsl:template match="tmpl[selector='tmBAR']">
        <mrow><mo>|</mo> <xsl:apply-templates select="slot[1] | pile[1]"/> <mo>|</mo></mrow>
    </xsl:template>

    <xsl:template match="tmpl[selector='tmBAR' and variation='tvLBAR']">
        <mrow>
            <mo>|</mo>
            <xsl:apply-templates select="slot[1] | pile[1]"/>
        </mrow>
    </xsl:template>

    <xsl:template match="tmpl[selector='tmBAR' and variation='tvRBAR']">
        <mrow>
            <xsl:apply-templates select="slot[1] | pile[1]"/>
            <mo>|</mo>
        </mrow>
    </xsl:template>

    <xsl:template match="tmpl[selector='tmFLOOR']">
        <mrow><mo>&#x230A;</mo> <xsl:apply-templates select="slot[1] | pile[1]"/> <mo>&#x230B;</mo></mrow>
    </xsl:template>

    <xsl:template match="tmpl[selector='tmCEILING']">
        <mrow><mo>&#x2308;</mo> <xsl:apply-templates select="slot[1] | pile[1]"/> <mo>&#x2309;</mo></mrow>
    </xsl:template>

    <!-- Interval brackets (v3: separate selectors per combination) -->
    <xsl:template match="tmpl[selector='tmLBLB']">
        <mrow><mo>[</mo> <xsl:apply-templates select="slot[1] | pile[1]"/> <mo>[</mo></mrow>
    </xsl:template>

    <xsl:template match="tmpl[selector='tmRBRB']">
        <mrow><mo>]</mo> <xsl:apply-templates select="slot[1] | pile[1]"/> <mo>]</mo></mrow>
    </xsl:template>

    <xsl:template match="tmpl[selector='tmRBLB']">
        <mrow><mo>]</mo> <xsl:apply-templates select="slot[1] | pile[1]"/> <mo>[</mo></mrow>
    </xsl:template>

    <xsl:template match="tmpl[selector='tmLBRP']">
        <mrow><mo>[</mo> <xsl:apply-templates select="slot[1] | pile[1]"/> <mo>)</mo></mrow>
    </xsl:template>

    <xsl:template match="tmpl[selector='tmLPRB']">
        <mrow><mo>(</mo> <xsl:apply-templates select="slot[1] | pile[1]"/> <mo>]</mo></mrow>
    </xsl:template>

    <xsl:template match="tmpl[selector='tmBRACK' and variation='tvLBRACK']">
        <mrow> <mo>[</mo> <xsl:apply-templates select="slot[1] | pile[1]"/> </mrow>
    </xsl:template>

    <xsl:template match="tmpl[selector='tmBRACK' and variation='tvRBRACK']">
        <mrow><xsl:apply-templates select="slot[1] | pile[1]"/> <mo>]</mo></mrow>
    </xsl:template>

    <xsl:template match="tmpl[selector='tmBRACE' and variation='tvLBRACE']">
        <mrow><mo>{</mo> <xsl:apply-templates select="slot[1] | pile[1]"/> </mrow>
    </xsl:template>

    <xsl:template match="tmpl[selector='tmBRACE' and variation='tvRBRACE']">
        <mrow><xsl:apply-templates select="slot[1] | pile[1]"/> <mo>}</mo></mrow>
    </xsl:template>

    <xsl:template match="tmpl[selector='tmDIRAC']">
        <mrow>
            <mo>&#x2329;</mo>
            <xsl:apply-templates select="slot[1] | pile[1]"/>
            <mo>|</mo>
            <xsl:apply-templates select="slot[2] | pile[2]"/>
            <mo>&#x232A;</mo>
        </mrow>
    </xsl:template>

    <xsl:template match="tmpl[selector='tmDIRAC' and variation='tvRDIRAC']">
        <mrow>
            <mo>|</mo>
            <xsl:apply-templates select="slot[2] | pile[2]"/>
            <mo>&#x232A;</mo>
        </mrow>
    </xsl:template>

    <xsl:template match="tmpl[selector='tmDIRAC' and variation='tvLDIRAC']">
        <mrow>
            <mo>&#x2329;</mo>
            <xsl:apply-templates select="slot[1] | pile[1]"/>
            <mo>|</mo>
        </mrow>
    </xsl:template>

    <xsl:template match="tmpl[selector='tmDBAR']">
        <mrow><mo>&#x2016;</mo> <xsl:apply-templates select="slot[1] | pile[1]"/> <mo>&#x2016;</mo></mrow>
    </xsl:template>

    <xsl:template match="tmpl[selector='tmDBAR' and variation='tvLDBAR']">
        <mrow>
            <mo>&#x2016;</mo>
            <xsl:apply-templates select="slot[1] | pile[1]"/>
        </mrow>
    </xsl:template>

    <xsl:template match="tmpl[selector='tmDBAR' and variation='tvRDBAR']">
        <mrow>
            <xsl:apply-templates select="slot[1] | pile[1]"/>
            <mo>&#x2016;</mo>
        </mrow>
    </xsl:template>

    <!-- Horizontal braces (v3: tmLHBRACE = underbrace, tmUHBRACE = overbrace) -->
    <xsl:template match="tmpl[selector='tmLHBRACE']">
        <munder>
            <munder>
                <xsl:apply-templates select="slot[1] | pile[1]"/>
                <mo stretchy="true">&#xFE38;</mo>
            </munder>
            <xsl:apply-templates select="slot[2] | pile[2]"/>
        </munder>
    </xsl:template>

    <xsl:template match="tmpl[selector='tmUHBRACE']">
        <mover>
            <mover>
                <xsl:apply-templates select="slot[1] | pile[1]"/>
                <mo stretchy="true">&#xFE37;</mo>
            </mover>
            <xsl:apply-templates select="slot[2] | pile[2]"/>
        </mover>
    </xsl:template>

</xsl:stylesheet>
