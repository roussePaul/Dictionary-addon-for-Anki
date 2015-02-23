import sys
import subprocess
if sys.platform != 'win32':
	from lxml import etree
	import libxml2

class XSLT:
	def __init__(self,xsltPath):
		if sys.platform == 'win32':
			self.proc = XSLT_Win(xsltPath)
		else:
			self.proc = XSLT_Lin(xsltPath)
			
	def apply(self,xml):
		return self.proc.apply(xml)
		
class XSLT_Win:
	def __init__(self,xsltPath):
		self.xsltPath = xsltPath
		
	def apply(self,xml):    
		xml_file = open('xml.tmp','w')
		xml_file.write(xml)
		xml_file.close()
		
		call2 = 'msxsl.exe xml.tmp '+ self.xsltPath +' -o out.tmp'
		subprocess.call(call2)
		
		with open('out.tmp','r') as content_file:
			result = content_file.read()
		
		return result.decode('UTF-16')

class XSLT_Lin:
	def __init__(self,xsltPath):
		style = etree.parse(xsltPath)
		self.style = etree.XSLT(style)
		
	def apply(self,data):
		result = self.style(etree.XML(data))
		return result
		