<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
	<xsl:output method="xml" indent="yes"/>


	<xsl:template match="/dictionary" >
		<xdxf format="logical">

			<xsl:attribute name="lang_from">
				<xsl:value-of select="@source-language" />
			</xsl:attribute>
			<xsl:attribute name="lang_from">
				<xsl:value-of select="@target-language" />
			</xsl:attribute>
			<xsl:attribute name="revision">
				<xsl:value-of select="@version" />
			</xsl:attribute>

			<meta_info>
				<title><xsl:value-of select="@name" /></title>
				<description><xsl:value-of select="@licenseComment" /></description>
				<file_ver><xsl:value-of select="@version" /></file_ver>
				<creation_date><xsl:value-of select="@created" /></creation_date>
				<dict_src_url><xsl:value-of select="@originURL" /></dict_src_url>
			</meta_info>

			<lexikon>
				<xsl:for-each select="word">
					<ar>

						<k>
							<xsl:value-of select="@value"/>
						</k>
						
						<def> 

							<xsl:attribute name="cmt">
								<xsl:value-of select="@comment" />
							</xsl:attribute>
							<gr type="class">
								<xsl:value-of select="@class"/>
							</gr>
						 	<xsl:for-each select="paradigm/inflection">
						 		<gr type="inflection">
									<xsl:value-of select="@value"/>
								</gr>
							</xsl:for-each>
						 	<xsl:for-each select="grammar">
						 		<gr type="info">
									<xsl:value-of select="@value"/>
								</gr>
							</xsl:for-each>
							
							<xsl:for-each select="translation">
								<dtrn>
									<xsl:value-of select="@value"/>
								</dtrn>
							</xsl:for-each>

							<tr>
								<xsl:value-of select="phonetique/@value"/>
							</tr>
							<sr>
								<xsl:for-each select="synonym">
									<kref type="syn">
										<xsl:value-of select="@value"/>
									</kref>
								</xsl:for-each>
							</sr>

							<xsl:for-each select="example">
								<ex type="exm">
									<ex_orig>
										<xsl:value-of select="@value"/>
									</ex_orig>
									<ex_transl>
										<xsl:value-of select="translation/@value"/>
									</ex_transl>
								</ex>
							</xsl:for-each>

							<xsl:for-each select="explanation">
								<co>
									<xsl:value-of select="@value"/> (<xsl:value-of select="translation/@value"/>)
								</co>
							</xsl:for-each>

							<xsl:for-each select="compound">
								<etm>
									<xsl:value-of select="@value"/> (<xsl:value-of select="translation/@value"/>)
								</etm>
							</xsl:for-each>

						</def>
					</ar>		
				</xsl:for-each>
			</lexikon>
		</xdxf>
	</xsl:template>


</xsl:stylesheet>
