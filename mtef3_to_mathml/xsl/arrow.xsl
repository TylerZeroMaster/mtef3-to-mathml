<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    exclude-result-prefixes="xs"
    version="1.0">

    <!-- Arrows with labels: arrow is base, slot[1] is the label above/below -->

    <xsl:template match="tmpl[selector='tmRARROW' and variation='tvRTARROW']">
        <mover>
            <mo stretchy="true">&#x2192;</mo>
            <xsl:apply-templates select="slot[1] | pile[1]"/>
        </mover>
    </xsl:template>

    <xsl:template match="tmpl[selector='tmRARROW' and variation='tvRBARROW']">
        <munder>
            <mo stretchy="true">&#x2192;</mo>
            <xsl:apply-templates select="slot[1] | pile[1]"/>
        </munder>
    </xsl:template>

    <xsl:template match="tmpl[selector='tmLARROW' and variation='tvLTARROW']">
        <mover>
            <mo stretchy="true">&#x2190;</mo>
            <xsl:apply-templates select="slot[1] | pile[1]"/>
        </mover>
    </xsl:template>

    <xsl:template match="tmpl[selector='tmLARROW' and variation='tvLBARROW']">
        <munder>
            <mo stretchy="true">&#x2190;</mo>
            <xsl:apply-templates select="slot[1] | pile[1]"/>
        </munder>
    </xsl:template>

    <xsl:template match="tmpl[selector='tmBARROW' and variation='tvBTARROW']">
        <mover>
            <mo stretchy="true">&#x2194;</mo>
            <xsl:apply-templates select="slot[1] | pile[1]"/>
        </mover>
    </xsl:template>

    <xsl:template match="tmpl[selector='tmBARROW' and variation='tvBBARROW']">
        <munder>
            <mo stretchy="true">&#x2194;</mo>
            <xsl:apply-templates select="slot[1] | pile[1]"/>
        </munder>
    </xsl:template>

    <!-- Vector arrows: expression is base (slot[1]), arrow is accent above/below -->

    <xsl:template match="tmpl[selector='tmOARROW' and variation='tvROARROW']">
        <mover>
            <xsl:apply-templates select="slot[1] | pile[1]"/>
            <mo stretchy="true">&#x2192;</mo>
        </mover>
    </xsl:template>

    <xsl:template match="tmpl[selector='tmOARROW' and variation='tvLOARROW']">
        <mover>
            <xsl:apply-templates select="slot[1] | pile[1]"/>
            <mo stretchy="true">&#x2190;</mo>
        </mover>
    </xsl:template>

    <xsl:template match="tmpl[selector='tmOARROW' and variation='tvDOARROW']">
        <mover>
            <xsl:apply-templates select="slot[1] | pile[1]"/>
            <mo stretchy="true">&#x2194;</mo>
        </mover>
    </xsl:template>

    <xsl:template match="tmpl[selector='tmUARROW' and variation='tvRUARROW']">
        <munder>
            <xsl:apply-templates select="slot[1] | pile[1]"/>
            <mo stretchy="true">&#x2192;</mo>
        </munder>
    </xsl:template>

    <xsl:template match="tmpl[selector='tmUARROW' and variation='tvLUARROW']">
        <munder>
            <xsl:apply-templates select="slot[1] | pile[1]"/>
            <mo stretchy="true">&#x2190;</mo>
        </munder>
    </xsl:template>

    <xsl:template match="tmpl[selector='tmUARROW' and variation='tvDUARROW']">
        <munder>
            <xsl:apply-templates select="slot[1] | pile[1]"/>
            <mo stretchy="true">&#x2194;</mo>
        </munder>
    </xsl:template>

</xsl:stylesheet>
