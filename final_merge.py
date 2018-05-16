from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QFormLayout, QPushButton, QAction, QLineEdit, QMessageBox, QScrollArea, QVBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
import sys
import re, string
import os
import argparse
import base64
import MySQLdb
import cStringIO
import PIL.Image
import re, string
import mysql.connector
import numpy as np
import re, math
from nltk.parse.stanford import StanfordParser
from nltk.parse.stanford import StanfordDependencyParser
from nltk.parse.stanford import StanfordNeuralDependencyParser
from nltk.tag.stanford import StanfordPOSTagger, StanfordNERTagger
from nltk.tokenize.stanford import StanfordTokenizer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from collections import Counter
from operator import itemgetter
from PIL import ImageFile
from rake_nltk import Rake


textObtained = ""
fin_list = []
WORD = re.compile(r'\w+')
k = 0

class Second(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(Second, self).__init__(parent)
        self.title = 'Trying UI'
        self.left = 10
        self.top = 10
        self.width = 500
        self.height = 500

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

class First(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(First, self).__init__(parent)
        self.title = 'Comic to Text Illustration'
        self.left = 10
        self.top = 10
        self.width = 500
        self.height = 500

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # Create textbox
        self.textbox = QLineEdit(self)
        self.textbox.move(20, 20)
        self.textbox.resize(200, 40)

        # add button
        self.addButton = QPushButton('Analyze')
        self.addButton.clicked.connect(self.on_click)
        self.addButton.move(20, 80)

        # del button
        self.delButton = QPushButton('Delete')
        self.delButton.clicked.connect(self.on_click_del)
        self.delButton.move(20, 100)

        # scroll area widget contents - layout
        self.scrollLayout = QFormLayout()

        # scroll area widget contents
        self.scrollWidget = QWidget()
        self.scrollWidget.setLayout(self.scrollLayout)

        # scroll area
        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.scrollWidget)

        # main layout
        self.mainLayout = QVBoxLayout()

        # add all main to the main vLayout
        self.mainLayout.addWidget(self.textbox)
        self.mainLayout.addWidget(self.addButton)
        self.mainLayout.addWidget(self.scrollArea)
        self.mainLayout.addWidget(self.delButton)

        # central widget
        self.centralWidget = QWidget()
        self.centralWidget.setLayout(self.mainLayout)

        # set central widget
        self.setCentralWidget(self.centralWidget)
        
    def on_click(self):
        textObtained = self.textbox.text()
        extraction(textObtained)
        i = 0
        while i < len(fin_list):
        			self.button = QPushButton(str(fin_list[i]))
        			self.scrollLayout.addRow(self.button)
        			i = i + 1

        for j in reversed(range(self.scrollLayout.count())):
                    self.scrollLayout.itemAt(j).widget().clicked.connect(lambda: request())

    def on_click_del(self):
        global k
    	self.textbox.setText("")
    	for i in reversed(range(self.scrollLayout.count())): 
    				self.scrollLayout.itemAt(i).widget().deleteLater()
        fin_list[:] = []
        k = 0

def request():
        global k
        test(fin_list[k])
        k = k + 1

# Used for u tags associated with elements of the sentence -----------------------

def get_continuous_chunks(tagged_sent):
    continuous_chunk = []
    current_chunk = []

    for token, tag in tagged_sent:
        if tag != "O":
            current_chunk.append((token, tag))
        else:
            if current_chunk: # if the current chunk is not empty
                continuous_chunk.append(current_chunk)
                current_chunk = []
    
    # Flush the final current_chunk into the continuous_chunk, if any.
    
    if current_chunk:
        continuous_chunk.append(current_chunk)
    return continuous_chunk

def extraction(s):
        # Locating the files on the system ---------------------------------------------

        a = set()
        b = set()
        posjar = '/Users/animesh/Desktop/Major/stanford-postagger-2017-06-09/stanford-postagger.jar'
        posmodel = '/Users/animesh/Desktop/Major/stanford-postagger-2017-06-09/models/english-left3words-distsim.tagger'
        nerjar = '/Users/animesh/Desktop/Major/stanford-ner-2017-06-09/stanford-ner.jar'
        nermodel = '/Users/animesh/Desktop/Major/stanford-ner-2017-06-09/classifiers/english.all.3class.distsim.crf.ser.gz'

        # Entity Extraction Code ------------------------------------------------------

        st = StanfordNERTagger(nermodel, nerjar, encoding='utf8') 
        str_chunk = re.split(r'(?<=\w\.)\s', s)
        i = 0
        j = 0
        for z in str_chunk:
            z = "".join(c for c in z if c not in ('!','.',':',','))
            ne_tagged_sent = st.tag(z.split())
            named_entities = get_continuous_chunks(ne_tagged_sent)
            named_entities = get_continuous_chunks(ne_tagged_sent)
            named_entities_str = [" ".join([token for token, tag in ne]) for ne in named_entities]
            named_entities_str_tag = [(" ".join([token for token, tag in ne]), ne[0][1]) for ne in named_entities]

            lstentities = []
            lstorg = []

            for x in named_entities_str_tag:
                y = str(x)
                y = y.replace("u'", "'")
                k = y.find(",", 2) + 3
                entity_type = y[k : y.find("'", k + 1)] 
                if entity_type == "PERSON":
                    lstentities.append(y[2 : y.find(",", 3) - 1])
                if entity_type == "ORGANIZATION":
                    lstorg.append(y[2 : y.find(",", 3) - 1])    

            for x in lstentities:
                print "Entity " + str(i + 1) + ": " + x
                i += 1
                a.add(x.lower())

            for x in lstorg:
                print "Organisation " + str(j + 1) + ": " + x
                j += 1
                a.add(x.lower())

            word = []
            tag = []

            for x in ne_tagged_sent:
                    y = str(x)
                    y = y.replace("u'", "'")
                    k = y.find(",", 2) + 3 
                    word.append(y[2 : y.find(",", 3) - 1])
                    tag.append(y[k : y.find("'", k + 1)])

        # Compound nature of the sentence

        analyzer = SentimentIntensityAnalyzer()
        vs = analyzer.polarity_scores(s)
        for k in sorted(vs):
                if k == "compound":
                        if vs[k] >= 0.5 :
                            print "positive"
                        elif vs[k] < 0.5 and vs[k] > -0.5 :
                            print "neutral"
                        elif vs[k] <= -0.5 :
                            print "negative"        

        # Keyword extraction using Rake

        r = Rake()
        r.extract_keywords_from_text(s)
        x = r.get_ranked_phrases()
        for i in x:
        	b.add(i.lower())
        interimList = list(set(a).union(set(b)))
        for i in interimList:
        	fin_list.append(i)

def write_file(data, filename):
    with open(filename, 'wb') as f:
        f.write(data)

def sort_list(li):
    li.sort(key = lambda x: x[1])
    return li

def get_cosine(vec1, vec2):
     intersection = set(vec1.keys()) & set(vec2.keys())
     numerator = sum([vec1[x] * vec2[x] for x in intersection])

     sum1 = sum([vec1[x]**2 for x in vec1.keys()])
     sum2 = sum([vec2[x]**2 for x in vec2.keys()])
     denominator = math.sqrt(sum1) * math.sqrt(sum2)

     if not denominator:
        return 0.0
     else:
        return float(numerator) / denominator

def text_to_vector(text):
     words = WORD.findall(text)
     return Counter(words)

def cool(id, searched_word):
	db = MySQLdb.connect("localhost","root","","major")
	cursor = db.cursor()
	cursor.execute("SELECT picture from info where srno = %s",(id,))
	data = cursor.fetchone()[0]
	dataconv = base64.b64decode(data + '=' * (-len(data) % 4))
	file = cStringIO.StringIO(dataconv)
	write_file(dataconv, "output/" + searched_word + str(id))

def test(searched_word):
	db = MySQLdb.connect("localhost","root","","major")
	cursor = db.cursor()
	vec_a = text_to_vector(searched_word)
	cursor.execute("SELECT count(*) from info",)
	ret = cursor.fetchall()
	t_sz = ret[0][0]
	i = 1
	k = 1
	x = []
	while t_sz:
			cursor.execute("SELECT tags from info where srno = %s",(i,))
			data = cursor.fetchall()
			vec_b = text_to_vector(data[0][0])
			sorted(vec_b.items(), key = itemgetter(0))
			cosine = get_cosine(vec_a, vec_b)
			if cosine > 0:
				x.append([i, cosine])		
			i = i + 1
			t_sz = t_sz - 1		
	sort_list(x)
	x = x[::-1]
	print "\n"
	print x
	print "\n"
	if x is not None:
		for m in x:
			if k <= 10:
				cool(m[0], searched_word)
				k += 1

def main():
    app = QtWidgets.QApplication(sys.argv)
    main = First()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()