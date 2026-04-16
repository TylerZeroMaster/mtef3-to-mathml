<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    exclude-result-prefixes="xs"
    version="1.0">

    <!-- Integral operators (tmINTOP): slot[2]=lower, slot[3]=upper, slot[4]=operator symbol -->

    <xsl:template match="tmpl[selector='tmINTOP' and variation='tvBINTOP']">
        <msubsup>
            <mstyle mathsize="140%" displaystyle="true"><xsl:apply-templates select="slot[4] | pile[4]"/></mstyle>
            <xsl:apply-templates select="slot[2] | pile[2]"/>
            <xsl:apply-templates select="slot[3] | pile[3]"/>
        </msubsup>
    </xsl:template>

    <xsl:template match="tmpl[selector='tmINTOP' and variation='tvUINTOP']">
        <msup>
            <mstyle mathsize="140%" displaystyle="true"><xsl:apply-templates select="slot[4] | pile[4]"/></mstyle>
            <xsl:apply-templates select="slot[3] | pile[3]"/>
        </msup>
    </xsl:template>

    <xsl:template match="tmpl[selector='tmINTOP' and variation='tvLINTOP']">
        <msub>
            <mstyle mathsize="140%" displaystyle="true"><xsl:apply-templates select="slot[4] | pile[4]"/></mstyle>
            <xsl:apply-templates select="slot[2] | pile[2]"/>
        </msub>
    </xsl:template>

    <!-- Single integrals (tmSINT): slot[1]=integrand, slot[2]=lower, slot[3]=upper -->

    <xsl:template match="tmpl[selector='tmSINT' and variation='tvNSINT']">
        <mstyle displaystyle="true">
            <mrow><mo>&#x222B;</mo>
                <xsl:apply-templates select="slot[1] | pile[1]"/>
            </mrow>
        </mstyle>
    </xsl:template>

    <xsl:template match="tmpl[selector='tmSINT' and variation='tvLSINT']">
        <mstyle displaystyle="true">
            <mrow>
                <msub>
                    <mo>&#x222B;</mo>
                    <xsl:apply-templates select="slot[2] | pile[2]"/>
                </msub>
                <xsl:apply-templates select="slot[1] | pile[1]"/>
            </mrow>
        </mstyle>
    </xsl:template>

    <xsl:template match="tmpl[selector='tmSINT' and variation='tvBSINT']">
        <mstyle displaystyle="true">
            <mrow>
                <msubsup>
                    <mo>&#x222B;</mo>
                    <xsl:apply-templates select="slot[2] | pile[2]"/>
                    <xsl:apply-templates select="slot[3] | pile[3]"/>
                </msubsup>
                <xsl:apply-templates select="slot[1] | pile[1]"/>
            </mrow>
        </mstyle>
    </xsl:template>

    <xsl:template match="tmpl[selector='tmSINT' and variation='tvNCINT']">
        <mstyle displaystyle="true">
            <mrow><mo>&#x222E;</mo>
                <xsl:apply-templates select="slot[1] | pile[1]"/>
            </mrow>
        </mstyle>
    </xsl:template>

    <xsl:template match="tmpl[selector='tmSINT' and variation='tvLCINT']">
        <mstyle displaystyle="true">
            <mrow>
                <msub>
                    <mo>&#x222E;</mo>
                    <xsl:apply-templates select="slot[2] | pile[2]"/>
                </msub>
                <xsl:apply-templates select="slot[1] | pile[1]"/>
            </mrow>
        </mstyle>
    </xsl:template>

    <!-- Double integrals (tmDINT) -->

    <xsl:template match="tmpl[selector='tmDINT' and variation='tvNDINT']">
        <mstyle displaystyle="true">
            <mrow><mo>&#x222C;</mo>
                <xsl:apply-templates select="slot[1] | pile[1]"/>
            </mrow>
        </mstyle>
    </xsl:template>

    <xsl:template match="tmpl[selector='tmDINT' and variation='tvLDINT']">
        <mstyle displaystyle="true">
            <mrow>
                <msub>
                    <mo>&#x222C;</mo>
                    <xsl:apply-templates select="slot[2] | pile[2]"/>
                </msub>
                <xsl:apply-templates select="slot[1] | pile[1]"/>
            </mrow>
        </mstyle>
    </xsl:template>

    <xsl:template match="tmpl[selector='tmDINT' and variation='tvNAINT']">
        <mstyle displaystyle="true">
            <mrow><mo>&#x222F;</mo>
                <xsl:apply-templates select="slot[1] | pile[1]"/>
            </mrow>
        </mstyle>
    </xsl:template>

    <xsl:template match="tmpl[selector='tmDINT' and variation='tvLAINT']">
        <mstyle displaystyle="true">
            <mrow>
                <msub>
                    <mo>&#x222F;</mo>
                    <xsl:apply-templates select="slot[2] | pile[2]"/>
                </msub>
                <xsl:apply-templates select="slot[1] | pile[1]"/>
            </mrow>
        </mstyle>
    </xsl:template>

    <!-- Triple integrals (tmTINT) -->

    <xsl:template match="tmpl[selector='tmTINT' and variation='tvNTINT']">
        <mstyle displaystyle="true">
            <mrow><mo>&#x222D;</mo>
                <xsl:apply-templates select="slot[1] | pile[1]"/>
            </mrow>
        </mstyle>
    </xsl:template>

    <xsl:template match="tmpl[selector='tmTINT' and variation='tvLTINT']">
        <mstyle displaystyle="true">
            <mrow>
                <msub>
                    <mo>&#x222D;</mo>
                    <xsl:apply-templates select="slot[2] | pile[2]"/>
                </msub>
                <xsl:apply-templates select="slot[1] | pile[1]"/>
            </mrow>
        </mstyle>
    </xsl:template>

    <xsl:template match="tmpl[selector='tmTINT' and variation='tvNVINT']">
        <mstyle displaystyle="true">
            <mrow><mo>&#x2230;</mo>
                <xsl:apply-templates select="slot[1] | pile[1]"/>
            </mrow>
        </mstyle>
    </xsl:template>

    <xsl:template match="tmpl[selector='tmTINT' and variation='tvLVINT']">
        <mstyle displaystyle="true">
            <mrow>
                <msub>
                    <mo>&#x2230;</mo>
                    <xsl:apply-templates select="slot[2] | pile[2]"/>
                </msub>
                <xsl:apply-templates select="slot[1] | pile[1]"/>
            </mrow>
        </mstyle>
    </xsl:template>

    <!-- Single surface/loop integrals (tmSSINT) -->

    <xsl:template match="tmpl[selector='tmSSINT' and variation='tvBSSINT']">
        <mstyle displaystyle="true">
            <mrow>
                <msubsup>
                    <mo>&#x222E;</mo>
                    <xsl:apply-templates select="slot[2] | pile[2]"/>
                    <xsl:apply-templates select="slot[3] | pile[3]"/>
                </msubsup>
                <xsl:apply-templates select="slot[1] | pile[1]"/>
            </mrow>
        </mstyle>
    </xsl:template>

    <xsl:template match="tmpl[selector='tmSSINT' and variation='tvLSSINT']">
        <mstyle displaystyle="true">
            <mrow>
                <msub>
                    <mo>&#x222E;</mo>
                    <xsl:apply-templates select="slot[2] | pile[2]"/>
                </msub>
                <xsl:apply-templates select="slot[1] | pile[1]"/>
            </mrow>
        </mstyle>
    </xsl:template>

    <xsl:template match="tmpl[selector='tmSSINT' and variation='tvLCSINT']">
        <mstyle displaystyle="true">
            <mrow>
                <msub>
                    <mo>&#x2232;</mo>
                    <xsl:apply-templates select="slot[2] | pile[2]"/>
                </msub>
                <xsl:apply-templates select="slot[1] | pile[1]"/>
            </mrow>
        </mstyle>
    </xsl:template>

    <!-- Double surface integrals (tmDSINT) -->

    <xsl:template match="tmpl[selector='tmDSINT' and variation='tvLASINT']">
        <mstyle displaystyle="true">
            <mrow>
                <msub>
                    <mo>&#x222F;</mo>
                    <xsl:apply-templates select="slot[2] | pile[2]"/>
                </msub>
                <xsl:apply-templates select="slot[1] | pile[1]"/>
            </mrow>
        </mstyle>
    </xsl:template>

    <xsl:template match="tmpl[selector='tmDSINT' and variation='tvLDSINT']">
        <mstyle displaystyle="true">
            <mrow>
                <msub>
                    <mo>&#x222C;</mo>
                    <xsl:apply-templates select="slot[2] | pile[2]"/>
                </msub>
                <xsl:apply-templates select="slot[1] | pile[1]"/>
            </mrow>
        </mstyle>
    </xsl:template>

    <!-- Triple surface integrals (tmTSINT) -->

    <xsl:template match="tmpl[selector='tmTSINT' and variation='tvLVSINT']">
        <mstyle displaystyle="true">
            <mrow>
                <msub>
                    <mo>&#x2230;</mo>
                    <xsl:apply-templates select="slot[2] | pile[2]"/>
                </msub>
                <xsl:apply-templates select="slot[1] | pile[1]"/>
            </mrow>
        </mstyle>
    </xsl:template>

    <xsl:template match="tmpl[selector='tmTSINT' and variation='tvLTSINT']">
        <mstyle displaystyle="true">
            <mrow>
                <msub>
                    <mo>&#x222D;</mo>
                    <xsl:apply-templates select="slot[2] | pile[2]"/>
                </msub>
                <xsl:apply-templates select="slot[1] | pile[1]"/>
            </mrow>
        </mstyle>
    </xsl:template>

</xsl:stylesheet>
