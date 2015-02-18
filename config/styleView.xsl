<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
	<xsl:output method="html" encoding="UTF-8" indent="yes" />
<xsl:template match="/ar" >
	<html>
		<b>
		<xsl:value-of select="k"/>
		</b>
		(<i>
		<xsl:value-of select="def/gr[@type='class']"/>
		</i>)
		<xsl:for-each select="def/gr[@type='inflection']">
			<xsl:choose>
				<xsl:when test="not(position() = last())"><xsl:value-of select="text()"/>
				<xsl:text>, </xsl:text>
				</xsl:when>
				<xsl:otherwise><xsl:value-of select="text()"/></xsl:otherwise>
			</xsl:choose>
		</xsl:for-each>
		: 

		<xsl:for-each select="def/dtrn">
			<xsl:choose>
				<xsl:when test="not(position() = last())"><xsl:value-of select="text()"/>
				<xsl:text>, </xsl:text>
				</xsl:when>
				<xsl:otherwise><xsl:value-of select="text()"/></xsl:otherwise>
			</xsl:choose>
		</xsl:for-each> 

		<br/>
		<xsl:for-each select="def/ex">
			"<xsl:value-of select="ex_orig"/>" (<i><xsl:value-of select="ex_transl"/></i>)
			<br/>
		</xsl:for-each> 
	</html>
</xsl:template>

</xsl:stylesheet>
