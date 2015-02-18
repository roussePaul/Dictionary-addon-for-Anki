import libxml2
import requests
import json
from xml.dom.minidom import parse, parseString

class Dictionary:
	def __init__(self,path):
		self.path = path
		# Load dictionaries
		self.doc_en_sv = libxml2.parseFile(self.path + "/dict/en_sv.xdxf")
		self.en_sv = self.doc_en_sv.xpathNewContext()
		self.doc_sv_en = libxml2.parseFile(self.path + "/dict/sv_en.xdxf")
		self.sv_en = self.doc_sv_en.xpathNewContext()
		self.lang_en_sv = self.en_sv.xpathEval('/xdxf/@lang_from')[0].content
		self.lang_sv_en = self.sv_en.xpathEval('/xdxf/@lang_from')[0].content

	def __del__(self):
		self.doc_en_sv.freeDoc()
		self.doc_sv_en.freeDoc()

	def queryDict(self,request,dico,lg):
		dicoResult = [];
		result = dico.xpathEval(request)
		for l in result:
			dicoResult.append(self.getObject(l,dico,lg))
		return dicoResult

	def query(self, name):

		request = '//k[text()="'+name+'"]/..'
		d1 = self.queryDict(request,self.en_sv,self.lang_en_sv)
		d2 = self.queryDict(request,self.sv_en,self.lang_en_sv)

		return d1+d2

	def getAllWords(self):
		return self.getAllWordsFromDict(self.en_sv) + self.getAllWordsFromDict(self.sv_en)


	def getAllWordsFromDict(self,dico):
		request = '//k/text()'
		result = dico.xpathEval(request)
		return [r.content for r in result]

	def getObject(self, xml, doc,lg):
		dico = {}
		dico["lang_from"] = doc.xpathEval('/xdxf/@lang_from')[0].content
		dico["lang_to"] = doc.xpathEval('/xdxf/@lang_to')[0].content
		root = doc.setContextNode(xml)
		dico["k"] = doc.xpathEval('k')[0].content
		gr = doc.xpathEval('def/gr')
		if len(gr):
			dico["gr"] = doc.xpathEval('def/gr')[0].content
		listDtrn =  doc.xpathEval('def/dtrn')
		dico["dtrn"] = [l.content for l in listDtrn]
		dico["xml"] = xml
		# listExOrig =  doc.xpathEval('def/ex/ex_orig')
		# listExTran =  doc.xpathEval('def/ex/ex_transl')
		# dico["ex"] = [[o.content,t.content] for o,t in zip(listExOrig,listExTran)]
		return dico


class OnLineDict:
	def __init__(self):
		self.urlSuggest = "http://folkets-lexikon.csc.kth.se/folkets/folkets/generatecompletion"

	def dataSuggest(self,word):
		return "7|0|7|http://folkets-lexikon.csc.kth.se/folkets/folkets/|72408650102EFF3C0092D16FF6C6E52F|se.algoritmica.folkets.client.ItemSuggestService|getSuggestions|se.algoritmica.folkets.client.ProposalRequest/3613917143|com.google.gwt.user.client.ui.SuggestOracle$Request/3707347745|"+word+"|1|2|3|4|1|5|5|0|6|5|7|"

	def suggest(self,word):
		d = self.dataSuggest(word)
		r = requests.post(self.urlSuggest, data = d)
		print r.text


class WebDictionary:
	def __init__(self):
		pass

	def suggestUrl(self,word):
		return "http://tyda.se/complete?word="+word+"&lang%\5B%\5D=en&lang%\5B%\5D=sv"

	def definitionUrl(self,word):
		return "http://tyda.se/search/"+word+"?lang[0]=en&lang[1]=sv"

	def query(self,word):
		self.url = self.definitionUrl(word)
		self.doc = requests.get(self.url).content
		parse_options = libxml2.HTML_PARSE_RECOVER + \
		libxml2.HTML_PARSE_NOERROR + \
		libxml2.HTML_PARSE_NOWARNING
		self.dom = libxml2.htmlReadDoc(self.doc, '', None, parse_options)
		results = self.dom.xpathEval('//div[@class="page-searchresult"]/div[@class="box box-searchresult"]')
		return results
	def getObject(self,doc,xml,lang_from,lang_to):
		root = doc.setContextNode(xml)
		res['word'] = doc.xpathEval('h2/b/text()')
		res['lang_from'] = lang_from
		res['class'] = doc.xpathEval('div[@class="word-class"]/text()')

		res['trans'] = doc.xpathEval('//ul[@class="list list-translations"]/li[@class="item"')
		res['lang_to'] = lang_to


# doc_sv_en = libxml2.parseFile("folkets_sv_en_public.xdxf")
# sv_en = doc_sv_en.xpathNewContext()
# doc_en_sv = libxml2.parseFile("folkets_en_sv_public.xdxf")
# en_sv = doc_en_sv.xpathNewContext()
# name = "about"
# request = '//k[text()="'+name+'"]/..'
# list = en_sv.xpathEval(request)

# for l in list:
# 	print l

