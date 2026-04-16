<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    exclude-result-prefixes="xs"
    version="1.0">

    <!-- Unions and intersections: slot[1]=body, slot[2]=lower, slot[3]=upper -->

    <xsl:template match="tmpl[selector='tmINTER' and variation='tvNINTER']">
        <mstyle displaystyle="true">
            <mo>&#x2229;</mo>
            <xsl:apply-templates select="slot[1] | pile[1]"/>
        </mstyle>
    </xsl:template>

    <xsl:template match="tmpl[selector='tmINTER' and variation='tvLINTER']">
        <mstyle displaystyle="true">
            <munder>
                <mo>&#x2229;</mo>
                <xsl:apply-templates select="slot[2] | pile[2]"/>
            </munder>
            <xsl:apply-templates select="slot[1] | pile[1]"/>
        </mstyle>
    </xsl:template>

    <xsl:template match="tmpl[selector='tmINTER' and variation='tvBINTER']">
        <mstyle displaystyle="true">
            <munderover>
                <mo>&#x2229;</mo>
                <xsl:apply-templates select="slot[2] | pile[2]"/>
                <xsl:apply-templates select="slot[3] | pile[3]"/>
            </munderover>
            <xsl:apply-templates select="slot[1] | pile[1]"/>
        </mstyle>
    </xsl:template>

    <!-- Inline intersection (sub/sup style) -->

    <xsl:template match="tmpl[selector='tmIINTER' and variation='tvLIINTER']">
        <mstyle displaystyle="true">
            <msub>
                <mo>&#x2229;</mo>
                <xsl:apply-templates select="slot[2] | pile[2]"/>
            </msub>
            <xsl:apply-templates select="slot[1] | pile[1]"/>
        </mstyle>
    </xsl:template>

    <xsl:template match="tmpl[selector='tmIINTER' and variation='tvBIINTER']">
        <mstyle displaystyle="true">
            <msubsup>
                <mo>&#x2229;</mo>
                <xsl:apply-templates select="slot[2] | pile[2]"/>
                <xsl:apply-templates select="slot[3] | pile[3]"/>
            </msubsup>
            <xsl:apply-templates select="slot[1] | pile[1]"/>
        </mstyle>
    </xsl:template>

    <xsl:template match="tmpl[selector='tmUNION' and variation='tvNUNION']">
        <mstyle displaystyle="true">
            <mo>&#x222A;</mo>
            <xsl:apply-templates select="slot[1] | pile[1]"/>
        </mstyle>
    </xsl:template>

    <xsl:template match="tmpl[selector='tmUNION' and variation='tvLUNION']">
        <mstyle displaystyle="true">
            <munder>
                <mo>&#x222A;</mo>
                <xsl:apply-templates select="slot[2] | pile[2]"/>
            </munder>
            <xsl:apply-templates select="slot[1] | pile[1]"/>
        </mstyle>
    </xsl:template>

    <xsl:template match="tmpl[selector='tmUNION' and variation='tvBUNION']">
        <mstyle displaystyle="true">
            <munderover>
                <mo>&#x222A;</mo>
                <xsl:apply-templates select="slot[2] | pile[2]"/>
                <xsl:apply-templates select="slot[3] | pile[3]"/>
            </munderover>
            <xsl:apply-templates select="slot[1] | pile[1]"/>
        </mstyle>
    </xsl:template>

    <!-- Inline union (sub/sup style) -->

    <xsl:template match="tmpl[selector='tmIUNION' and variation='tvLIUNION']">
        <mstyle displaystyle="true">
            <msub>
                <mo>&#x222A;</mo>
                <xsl:apply-templates select="slot[2] | pile[2]"/>
            </msub>
            <xsl:apply-templates select="slot[1] | pile[1]"/>
        </mstyle>
    </xsl:template>

    <xsl:template match="tmpl[selector='tmIUNION' and variation='tvBIUNION']">
        <mstyle displaystyle="true">
            <msubsup>
                <mo>&#x222A;</mo>
                <xsl:apply-templates select="slot[2] | pile[2]"/>
                <xsl:apply-templates select="slot[3] | pile[3]"/>
            </msubsup>
            <xsl:apply-templates select="slot[1] | pile[1]"/>
        </mstyle>
    </xsl:template>

</xsl:stylesheet>
