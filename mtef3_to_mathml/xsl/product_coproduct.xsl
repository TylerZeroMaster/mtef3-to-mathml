<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    exclude-result-prefixes="xs"
    version="1.0">

    <!-- Product: slot[1]=body, slot[2]=lower, slot[3]=upper -->

    <xsl:template match="tmpl[selector='tmPROD' and variation='tvNPROD']">
        <mstyle displaystyle="true">
            <mo>&#x220F;</mo>
            <xsl:apply-templates select="slot[1] | pile[1]"/>
        </mstyle>
    </xsl:template>

    <xsl:template match="tmpl[selector='tmPROD' and variation='tvLPROD']">
        <mstyle displaystyle="true">
            <munder>
                <mo>&#x220F;</mo>
                <xsl:apply-templates select="slot[2] | pile[2]"/>
            </munder>
            <xsl:apply-templates select="slot[1] | pile[1]"/>
        </mstyle>
    </xsl:template>

    <xsl:template match="tmpl[selector='tmPROD' and variation='tvBPROD']">
        <mstyle displaystyle="true">
            <munderover>
                <mo>&#x220F;</mo>
                <xsl:apply-templates select="slot[2] | pile[2]"/>
                <xsl:apply-templates select="slot[3] | pile[3]"/>
            </munderover>
            <xsl:apply-templates select="slot[1] | pile[1]"/>
        </mstyle>
    </xsl:template>

    <!-- Inline product (sub/sup style) -->

    <xsl:template match="tmpl[selector='tmIPROD' and variation='tvLIPROD']">
        <mstyle displaystyle="true">
            <msub>
                <mo>&#x220F;</mo>
                <xsl:apply-templates select="slot[2] | pile[2]"/>
            </msub>
            <xsl:apply-templates select="slot[1] | pile[1]"/>
        </mstyle>
    </xsl:template>

    <xsl:template match="tmpl[selector='tmIPROD' and variation='tvBIPROD']">
        <mstyle displaystyle="true">
            <msubsup>
                <mo>&#x220F;</mo>
                <xsl:apply-templates select="slot[2] | pile[2]"/>
                <xsl:apply-templates select="slot[3] | pile[3]"/>
            </msubsup>
            <xsl:apply-templates select="slot[1] | pile[1]"/>
        </mstyle>
    </xsl:template>

    <!-- Coproduct -->

    <xsl:template match="tmpl[selector='tmCOPROD' and variation='tvNCOPROD']">
        <mstyle displaystyle="true">
            <mo>&#x2210;</mo>
            <xsl:apply-templates select="slot[1] | pile[1]"/>
        </mstyle>
    </xsl:template>

    <xsl:template match="tmpl[selector='tmCOPROD' and variation='tvLCOPROD']">
        <mstyle displaystyle="true">
            <munder>
                <mo>&#x2210;</mo>
                <xsl:apply-templates select="slot[2] | pile[2]"/>
            </munder>
            <xsl:apply-templates select="slot[1] | pile[1]"/>
        </mstyle>
    </xsl:template>

    <xsl:template match="tmpl[selector='tmCOPROD' and variation='tvBCOPROD']">
        <mstyle displaystyle="true">
            <munderover>
                <mo>&#x2210;</mo>
                <xsl:apply-templates select="slot[2] | pile[2]"/>
                <xsl:apply-templates select="slot[3] | pile[3]"/>
            </munderover>
            <xsl:apply-templates select="slot[1] | pile[1]"/>
        </mstyle>
    </xsl:template>

    <!-- Inline coproduct (sub/sup style) -->

    <xsl:template match="tmpl[selector='tmICOPROD' and variation='tvLICOPROD']">
        <mstyle displaystyle="true">
            <msub>
                <mo>&#x2210;</mo>
                <xsl:apply-templates select="slot[2] | pile[2]"/>
            </msub>
            <xsl:apply-templates select="slot[1] | pile[1]"/>
        </mstyle>
    </xsl:template>

    <xsl:template match="tmpl[selector='tmICOPROD' and variation='tvBICOPROD']">
        <mstyle displaystyle="true">
            <msubsup>
                <mo>&#x2210;</mo>
                <xsl:apply-templates select="slot[2] | pile[2]"/>
                <xsl:apply-templates select="slot[3] | pile[3]"/>
            </msubsup>
            <xsl:apply-templates select="slot[1] | pile[1]"/>
        </mstyle>
    </xsl:template>

</xsl:stylesheet>
