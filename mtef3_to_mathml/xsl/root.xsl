<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    exclude-result-prefixes="xs"
    version="1.0">

    <!-- Square root. slot[2] (the index) is always present but empty for
         tvSQROOT, so it's dropped rather than emitted as an empty child. -->
    <xsl:template match="tmpl[selector='tmROOT' and variation='tvSQROOT']">
        <msqrt>
            <xsl:apply-templates select="slot[1] | pile[1]"/>
        </msqrt>
    </xsl:template>

    <!-- Nth root: slot[1] = radicand, slot[2] = index. -->
    <xsl:template match="tmpl[selector='tmROOT' and variation='tvNTHROOT']">
        <mroot>
            <xsl:apply-templates select="slot[1] | pile[1]"/>
            <xsl:apply-templates select="slot[2] | pile[2]"/>
        </mroot>
    </xsl:template>

</xsl:stylesheet>
