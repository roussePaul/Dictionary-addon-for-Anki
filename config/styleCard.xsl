<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
	<xsl:output method="text" indent="no"/>
<xsl:template match="/ar" >
	<xsl:for-each select="def/dtrn">
		<xsl:choose>
			<xsl:when test="not(position() = last())"><xsl:value-of select="text()"/>
			<xsl:text>, </xsl:text>
			</xsl:when>
			<xsl:otherwise><xsl:value-of select="text()"/></xsl:otherwise>
		</xsl:choose>
	</xsl:for-each>
	<xsl:text>&#x9;</xsl:text>
	<xsl:value-of select="k"/>
	<xsl:if test="def/gr[not(@type='info')]/text() != ''">
		<xsl:text> (</xsl:text>
		<xsl:for-each select="def/gr[not(@type='info')]">
			<xsl:choose>
				<xsl:when test="not(position() = last())"><xsl:value-of select="text()"/>
				<xsl:text>, </xsl:text>
				</xsl:when>
				<xsl:otherwise><xsl:value-of select="text()"/></xsl:otherwise>
			</xsl:choose>
		</xsl:for-each>
		<xsl:text>)</xsl:text>
	</xsl:if>
</xsl:template>

</xsl:stylesheet>
