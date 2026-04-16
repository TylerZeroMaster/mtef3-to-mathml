<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    exclude-result-prefixes="xs"
    version="1.0">

     <!-- Fractions -->

     <xsl:template match="tmpl[selector='tmFRACT']">
        <mfrac>
            <xsl:apply-templates select="slot[1] | pile[1]"/>
            <xsl:apply-templates select="slot[2] | pile[2]"/>
        </mfrac>
    </xsl:template>

    <xsl:template match="tmpl[selector='tmFRACT' and variation='tvPFRACT']">
        <mstyle scriptlevel="+1">
            <mfrac>
                <xsl:apply-templates select="slot[1] | pile[1]"/>
                <xsl:apply-templates select="slot[2] | pile[2]"/>
            </mfrac>
        </mstyle>
    </xsl:template>

    <!-- Slant (bevelled) fractions -->

    <xsl:template match="tmpl[selector='tmSLFRACT']">
        <mfrac bevelled="true">
            <xsl:apply-templates select="slot[1] | pile[1]"/>
            <xsl:apply-templates select="slot[2] | pile[2]"/>
        </mfrac>
    </xsl:template>

</xsl:stylesheet>
