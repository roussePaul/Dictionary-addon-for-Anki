import xml.etree.ElementTree as ET
from xml.dom.minidom import parse, parseString

class Dictionary:
	def __init__(self,path):
		self.path = path
		# Load dictionaries
		self.dict_en_sv_path = self.path + "/dict/en_sv.xdxf"
		self.doc_en_sv = ET.parse(self.dict_en_sv_path)
		self.en_sv = self.doc_en_sv.getroot()
		self.en_sv_elements = self.doc_en_sv.findall(".//k/..")
		self.lang_en_sv = self.en_sv.attrib["lang_from"]

		self.dict_sv_en_path = self.path + "/dict/sv_en.xdxf"
		self.doc_sv_en = ET.parse(self.dict_sv_en_path)
		self.sv_en = self.doc_sv_en.getroot()
		self.sv_en_elements = self.doc_sv_en.findall(".//k/..")
		self.lang_sv_en = self.sv_en.attrib["lang_from"]

	def __del__(self):
		pass

	def queryDict(self,name,elements,dico):
		dicoResult = [];
		result = [x for x in elements if x.findtext('.//k').encode("UTF-8") == name]
		for l in result:
			dicoResult.append(self.getObject(l,dico))
		return dicoResult

	def query(self, name):

		d1 = self.queryDict(name,self.en_sv_elements,self.sv_en)
		d2 = self.queryDict(name,self.sv_en_elements,self.en_sv)

		return d1+d2

	def getAllWords(self):
		return self.getAllWordsFromDict(self.en_sv_elements) + self.getAllWordsFromDict(self.sv_en_elements)


	def getAllWordsFromDict(self,elements):
		result =  [x.findtext('.//k').encode("UTF-8") for x in elements]
		return result

	def getObject(self, node, doc):
		dico = {}
		dico["lang_from"] = doc.attrib["lang_to"]
		dico["lang_to"] = doc.attrib["lang_from"]
		dico["xml"] = ET.tostring(node)

		dico["k"] = node.findtext('.//k')
		dico["gr"] = node.findtext('.//def/gr')
		dico["dtrn"] = [l.text for l in node.findall('.//def/dtrn')]
		return dico


# doc_sv_en = libxml2.parseFile("folkets_sv_en_public.xdxf")
# sv_en = doc_sv_en.xpathNewContext()
# doc_en_sv = libxml2.parseFile("folkets_en_sv_public.xdxf")
# en_sv = doc_en_sv.xpathNewContext()
# name = "about"
# request = '//k[text()="'+name+'"]/..'
# list = en_sv.xpathEval(request)

# for l in list:
# 	print l

