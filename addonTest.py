# import the main window object (mw) from ankiqt
from aqt import mw
# import the "show info" tool from utils.py
from aqt.utils import showInfo, tooltip, openFolder, isWin
# import all of the Qt GUI library
from aqt.qt import *
import aqt.editor, aqt.modelchooser, aqt.deckchooser
from anki.importing import TextImporter
import sys, os, traceback

import dictionary

from lxml import etree
import libxml2


# We're going to add a menu item below. First we want to create a function to
# be called when the menu item is activated.
class DefinitionList(QListWidget):
	def __init__(self, dico):
		QListWidget.__init__(self)
		self.dico = dico
		
	def keyPressEvent(self, event):
		if type(event) == QKeyEvent:
			if event.key() == Qt.Key_Return :
				self.dico.addDefinition()
				self.dico.gotoQuery()
			elif event.key() < 0xFF:
				self.dico.gotoQuery(event)
			else:
				super(QListWidget, self).keyPressEvent(event)
		else:
			super(QListWidget, self).keyPressEvent(event)


class DicoWidget(QWidget):

	def __init__(self,mw):
		## GUI initialisation
		super(DicoWidget, self).__init__()
		box = QGridLayout(self)

		QTextCodec.setCodecForTr(QTextCodec.codecForName("UTF-8"))  
		QTextCodec.setCodecForCStrings(QTextCodec.codecForName("UTF-8"))  
		QTextCodec.setCodecForLocale(QTextCodec.codecForName("UTF-8"))  
		

		# initialisation
		self.mw = mw
		self.path = self.addonsFolder()
		
		# Query widget
		self.countLabel = QLCDNumber()
		self.countLabel.setFrameStyle(QFrame.NoFrame)
		self.countLabel.display(0)
		self.tQuery = QLineEdit()
		self.tQuery.returnPressed.connect(self.query)
		box.addWidget(self.tQuery,1,0,1,1)
		box.addWidget(self.countLabel,1,1,1,1)

		# Result list
		self.listResult = DefinitionList(self)
		self.listResult.itemSelectionChanged.connect(self.definitionView)
		box.addWidget(self.listResult,2,0,4,1)

		# Definition panel
		self.tDefinition = QPlainTextEdit()
		self.tDefinition.document().setMetaInformation( QTextDocument.DocumentUrl, self.path + "/" )
		box.addWidget(self.tDefinition,2,1,4,4)

		# self.bAdd = QPushButton('Add')
		# self.bAdd.clicked.connect(self.addDefinition)
		# box.addWidget(self.bAdd,6,0)

		# self.bSync = QPushButton('Synchronize')
		# self.bSync.clicked.connect(self.synchronize)
		# box.addWidget(self.bSync,6,1)

		# Model Chooser
		self.modelArea = QWidget()
		box.addWidget(self.modelArea,6,1)
		self.modelChooser = aqt.modelchooser.ModelChooser(self.mw, self.modelArea)


		# Deck Chooser
		self.deckArea = QWidget()
		box.addWidget(self.deckArea,6,0)
		self.deckChooser = aqt.deckchooser.DeckChooser(self.mw, self.deckArea)

		# Widget
		self.setGeometry(300, 300, 400, 400)
		self.show()

		# init file
		self.initTempFile()

		## Dictionary
		self.dico = dictionary.Dictionary(self.path)

		self.initSuggestion()
		self.initRenderCard()

	def initTempFile(self):
		## Temp file for new words
		self.filename = "new_words.tmp"
		self.file = open(self.filename,"w")
		self.nbreAdded = 0


	def setList(self,results):
		self.listResult.clear()
		for l in results:
			(f1,f2) = self.getFields(l)
			item = QListWidgetItem(f1+": "+f2)
			item.setIcon(self.getIconFromLanguage(l["lang_from"]));
			self.listResult.addItem(item)
			item.setData(Qt.UserRole, l)
		self.listResult.setFocus()

	def getIconFromLanguage(self,lg):
		return QIcon(self.path + "/flags/"+lg+".png")

	def query(self):
		request = self.tQuery.text()
		results = self.dico.query(request.encode("UTF-8"))
		self.setList(results)
		if len(results):
			self.gotoList()
		else:
			self.gotoQuery()

	def initSuggestion(self):
		self.listWords = self.dico.getAllWords()
		self.listWords = list(set(self.listWords))
		self.listWords.sort()
		self.completer = QCompleter(self.listWords,self.tQuery)
		self.tQuery.setCompleter(self.completer)


	def getSelection(self):
		item = self.listResult.currentItem()
		data = item.data(Qt.UserRole)
		return data

	def getFields(self,data):
		field1 = data["k"]
		if 'gr' in data.keys():
			field1 = field1 +" ("+data["gr"]+")"
		field2 = ""
		if len(data["dtrn"]):
			for dtrn in data["dtrn"][:-1]:
				field2 = field2 + dtrn + ", "
			field2 = field2 + data["dtrn"][-1]
		return (field1,field2)

	def definitionView(self):
		selectedCard = self.getSelection()
		card = self.renderView(selectedCard).__str__()
		print card
		self.tDefinition.appendHtml(card)

	def addDefinition(self):
		selectedCard = self.getSelection()
		card = self.renderCard(selectedCard).__str__()
		self.file.write(card+ "\n")
		self.nbreAdded = self.nbreAdded + 1
		self.countLabel.display(str(self.nbreAdded))
		tooltip(_(card.decode("UTF-8") + " added"), period=1000)

	def gotoQuery(self,event=None):
		self.tQuery.setFocus()
		self.tQuery.selectAll()
		if event!=None:
			self.tQuery.keyPressEvent(event)

	def gotoList(self):
		self.listResult.setFocus()
		self.listResult.setCurrentRow(0)


	def synchronize(self):
		if self.nbreAdded==0:
			tooltip(_("Nothing to synchronize"), period=1000)
			return

		self.file.close()
		# select deck
		did = self.deckChooser.selectedId()
		mw.col.decks.select(did)

		# import into the collection
		ti = TextImporter(mw.col, self.filename)

		ti.delimiter = '\t'
		ti.initMapping()

		if did != ti.model['did']:
			ti.model['did'] = did
			mw.col.models.save(ti.model)
			
		ti.run()

		self.initTempFile()

		tooltip(_("Synchronized"), period=1000)

		self.countLabel.display(str(self.nbreAdded))

		self.mw.reset()

	def initRenderCard(self):
		styledoc = etree.parse(self.path + "/config/styleCard.xsl")
		self.style = etree.XSLT(styledoc)
		styledoc = etree.parse(self.path + "/config/styleView.xsl")
		self.styleView = etree.XSLT(styledoc)

	def renderCard(self,data):
		result = self.style(etree.XML(data["xml"].__str__()))
		return result

	def renderView(self,data):
		result = self.styleView(etree.XML(data["xml"].__str__()))
		return result

	def close(self):
		self.synchronize()
		self.file.close()
		self.modelChooser.cleanup()
		self.deckChooser.cleanup()

	def closeEvent(self,event):
		self.close()
		
	def addonsFolder(self):
		dir = self.mw.pm.addonFolder()
		if isWin:
			dir = dir.encode(sys.getfilesystemencoding())
		return dir






def startDictionary():
	mw.myWidget = dico = DicoWidget(mw)

# create a new menu item, "test"
action = QAction("Dictionnaire", mw)
# set it to call testFunction when it's clicked
mw.connect(action, SIGNAL("triggered()"), startDictionary)
action.setShortcut(QKeySequence("Ctrl+T"))

# and add it to the tools menu
mw.form.menuTools.addAction(action)
