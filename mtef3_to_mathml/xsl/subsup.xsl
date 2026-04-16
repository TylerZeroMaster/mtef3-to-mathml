<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    exclude-result-prefixes="xs"
    version="1.0">

    <xsl:template match="tmpl[selector='tmSCRIPT' and variation='tvSUPER']">
        <msup>
            <xsl:apply-templates select="slot[1] | pile[1]"/>
            <xsl:apply-templates select="slot[3] | pile[3]"/>
        </msup>
    </xsl:template>

    <xsl:template match="tmpl[selector='tmSCRIPT' and variation='tvSUB']">
        <msub>
            <xsl:apply-templates select="slot[1] | pile[1]"/>
            <xsl:apply-templates select="slot[2] | pile[2]"/>
        </msub>
    </xsl:template>

    <xsl:template match="tmpl[selector='tmSCRIPT' and variation='tvSUBSUP']">
        <msubsup>
            <xsl:apply-templates select="slot[1] | pile[1]"/>
            <xsl:apply-templates select="slot[2] | pile[2]"/>
            <xsl:apply-templates select="slot[3] | pile[3]"/>
        </msubsup>
    </xsl:template>

    <xsl:template match="tmpl[selector='tmLSCRIPT' and variation='tvLSUPER']">
        <mmultiscripts>
            <xsl:apply-templates select="slot[1] | pile[1]"/>
            <mprescripts/>
            <none/>
            <xsl:apply-templates select="slot[3] | pile[3]"/>
        </mmultiscripts>
    </xsl:template>

    <xsl:template match="tmpl[selector='tmLSCRIPT' and variation='tvLSUB']">
        <mmultiscripts>
            <xsl:apply-templates select="slot[1] | pile[1]"/>
            <mprescripts/>
            <xsl:apply-templates select="slot[2] | pile[2]"/>
            <none/>
        </mmultiscripts>
    </xsl:template>

    <xsl:template match="tmpl[selector='tmLSCRIPT' and variation='tvLSUBSUP']">
        <mmultiscripts>
            <xsl:apply-templates select="slot[1] | pile[1]"/>
            <mprescripts/>
            <xsl:apply-templates select="slot[2] | pile[2]"/>
            <xsl:apply-templates select="slot[3] | pile[3]"/>
        </mmultiscripts>
    </xsl:template>
</xsl:stylesheet>
