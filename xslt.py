import sys
import subprocess
import os
import tempfile
if sys.platform != 'win32':
	from lxml import etree
	import libxml2

class XSLT:
	def __init__(self,path,xsltPath):
		if sys.platform == 'win32':
			self.proc = XSLT_Win(path,xsltPath)
		else:
			self.proc = XSLT_Lin(path,xsltPath)
			
	def apply(self,xml):
		return self.proc.apply(xml)
		
class XSLT_Win:
	def __init__(self,path,xsltPath):
		self.xsltPath = xsltPath
		self.tempPath = tempfile.gettempdir()
		self.pathExe = path
		self.xmlPath = self.tempPath + '\\xml.tmp'
		self.outPath = self.tempPath + '\\out.tmp'
		
	def apply(self,xml):	
		xml_file = open(self.xmlPath,'w')
		xml_file.write(xml)
		xml_file.close()
		
		commande = self.pathExe + '\\msxsl.exe '+self.xmlPath + ' ' + self.xsltPath +' -o '+self.outPath
		startupinfo = subprocess.STARTUPINFO()
		startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
		startupinfo.wShowWindow = subprocess.SW_HIDE
		proc = subprocess.Popen(commande,  startupinfo=startupinfo)
		proc.wait()
		
		with open(self.outPath,'r') as content_file:
			result = content_file.read()
		
		return result.decode("UTF-16",errors='replace')

class XSLT_Lin:
	def __init__(self,path,xsltPath):
		style = etree.parse(xsltPath)
		self.style = etree.XSLT(style)
		
	def apply(self,data):
		result = self.style(etree.XML(data))
		return result.decode("UTF-8")

