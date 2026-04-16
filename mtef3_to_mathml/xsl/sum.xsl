<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    exclude-result-prefixes="xs"
    version="1.0">

    <!-- Summations: slot[1]=body, slot[2]=lower, slot[3]=upper -->

    <xsl:template match="tmpl[selector='tmSUM' and variation='tvNSUM']">
        <mstyle displaystyle="true">
            <mo>&#x2211;</mo>
            <xsl:apply-templates select="slot[1] | pile[1]"/>
        </mstyle>
    </xsl:template>

    <xsl:template match="tmpl[selector='tmSUM' and variation='tvLSUM']">
        <mstyle displaystyle="true">
            <munder>
                <mo>&#x2211;</mo>
                <xsl:apply-templates select="slot[2] | pile[2]"/>
            </munder>
            <xsl:apply-templates select="slot[1] | pile[1]"/>
        </mstyle>
    </xsl:template>

    <xsl:template match="tmpl[selector='tmSUM' and variation='tvBSUM']">
        <mstyle displaystyle="true">
            <munderover>
                <mo>&#x2211;</mo>
                <xsl:apply-templates select="slot[2] | pile[2]"/>
                <xsl:apply-templates select="slot[3] | pile[3]"/>
            </munderover>
            <xsl:apply-templates select="slot[1] | pile[1]"/>
        </mstyle>
    </xsl:template>

    <!-- Inline sum (sub/sup style) -->

    <xsl:template match="tmpl[selector='tmISUM' and variation='tvLISUM']">
        <mstyle displaystyle="true">
            <msub>
                <mo>&#x2211;</mo>
                <xsl:apply-templates select="slot[2] | pile[2]"/>
            </msub>
            <xsl:apply-templates select="slot[1] | pile[1]"/>
        </mstyle>
    </xsl:template>

    <xsl:template match="tmpl[selector='tmISUM' and variation='tvBISUM']">
        <mstyle displaystyle="true">
            <msubsup>
                <mo>&#x2211;</mo>
                <xsl:apply-templates select="slot[2] | pile[2]"/>
                <xsl:apply-templates select="slot[3] | pile[3]"/>
            </msubsup>
            <xsl:apply-templates select="slot[1] | pile[1]"/>
        </mstyle>
    </xsl:template>

    <!-- Sum operator: slot[2]=lower, slot[3]=upper, slot[4]=operator symbol -->

    <xsl:template match="tmpl[selector='tmSUMOP' and variation='tvBSUMOP']">
        <munderover>
            <mstyle mathsize="140%" displaystyle="true"><xsl:apply-templates select="slot[4] | pile[4]"/></mstyle>
            <xsl:apply-templates select="slot[2] | pile[2]"/>
            <xsl:apply-templates select="slot[3] | pile[3]"/>
        </munderover>
    </xsl:template>

    <xsl:template match="tmpl[selector='tmSUMOP' and variation='tvUSUMOP']">
        <mover>
            <mstyle mathsize="140%" displaystyle="true"><xsl:apply-templates select="slot[4] | pile[4]"/></mstyle>
            <xsl:apply-templates select="slot[3] | pile[3]"/>
        </mover>
    </xsl:template>

    <xsl:template match="tmpl[selector='tmSUMOP' and variation='tvLSUMOP']">
        <munder>
            <mstyle mathsize="140%" displaystyle="true"><xsl:apply-templates select="slot[4] | pile[4]"/></mstyle>
            <xsl:apply-templates select="slot[2] | pile[2]"/>
        </munder>
    </xsl:template>

</xsl:stylesheet>
