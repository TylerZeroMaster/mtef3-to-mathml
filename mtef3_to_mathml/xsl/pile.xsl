<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    exclude-result-prefixes="xs"
    version="1.0">

    <!-- The translation of a pile using this form of translation string is performed with the following steps:

    The <start> part of the translation string is output;
    The first line is translated;
    The <repeat> part of the translation string is output;
    The next line is translated;
    If there are any more lines, go back to Step 3. Otherwise, continue with the next step;
    The <end> part of the translation string is output.
    -->
    <!-- Serializes a RULER's tab stops (if any) as "type:offset;type:offset;..."
         onto the current result element, so a tab-delimited pile/slot can be
         reconstructed into columns from the MathML output alone. -->
    <xsl:template name="tab-stops-attribute">
        <xsl:param name="ruler" select="ruler"/>
        <xsl:if test="$ruler">
            <xsl:attribute name="data-tab-stops">
                <xsl:for-each select="$ruler/tab_stop">
                    <xsl:value-of select="tab_type"/>
                    <xsl:text>:</xsl:text>
                    <xsl:value-of select="offset"/>
                    <xsl:if test="position() != last()">
                        <xsl:text>;</xsl:text>
                    </xsl:if>
                </xsl:for-each>
            </xsl:attribute>
        </xsl:if>
    </xsl:template>

    <xsl:template match="pile">
        <mtable>
            <xsl:call-template name="tab-stops-attribute"/>
            <xsl:apply-templates select="slot" mode="wrap"/>
        </mtable>
    </xsl:template>

    <xsl:template match="pile[halign='left']">
        <mtable columnalign="left">
            <xsl:call-template name="tab-stops-attribute"/>
            <xsl:apply-templates select="slot" mode="wrap"/>
        </mtable>
    </xsl:template>

    <xsl:template match="pile/slot" mode="wrap">
        <mtr>
            <xsl:call-template name="tab-stops-attribute"/>
            <mtd>
                <xsl:apply-templates select="."/>
            </mtd>
        </mtr>
    </xsl:template>

    <xsl:template match="pile[halign='right']">
        <mtable columnalign="right">
            <xsl:call-template name="tab-stops-attribute"/>
            <xsl:apply-templates select="slot" mode="wrap"/>
        </mtable>
    </xsl:template>

    <xsl:template match="pile[halign='decimal']">
        <mtable groupalign="decimalpoint">
            <xsl:call-template name="tab-stops-attribute"/>
            <xsl:apply-templates select="slot" mode="wrap"/>
        </mtable>
    </xsl:template>

    <xsl:template match="pile[halign='relational']">
        <mtable>
            <xsl:call-template name="tab-stops-attribute"/>
            <xsl:apply-templates select="slot" mode="wrap"/>
        </mtable>
    </xsl:template>

</xsl:stylesheet>
