# -*- coding: utf-8 -*-
from xml.etree import ElementTree as ET
import csv
import nltk
nltk.download('stopwords')
nltk.download('punkt')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

stop = stopwords.words("english")
ponctuation = [".", ",", ":",]

def isNumber(n):
    try:
        float(n)
        return True
    except ValueError:
        return False

class ListaInvertida:
    
    def __init__(self):
        self.words = {}
        
        
    def generate(self, file_to_read):
        root = ET.parse(file_to_read).getroot()
        records = self.getTokensByRecord(root)
        for key, value in records.items():
            self.getInvertedList(key, value)
        print(self.words)

    
    def getTokensByRecord(self, root):
        data = {}
        for record in root.findall("RECORD"):
            record_num = int(record.find("RECORDNUM").text.strip())
            abstract = record.find("ABSTRACT")
            
            if (abstract is not None):
                abstract_text = abstract.text.strip()
            else:
                extract = record.find("EXTRACT")
                if (extract is not None):
                    abstract_text = extract.text.strip()
                else: 
                    # If the document doesn't have either ABSTRACT or EXTRACT
                    continue 
            data[record_num] = self.getTokensFromAbstract(abstract_text)
        return data
    
    def getTokensFromAbstract(self, abstract):
        tokens = word_tokenize(abstract)
        alpha_tokens = [token for token in tokens if token.isalpha()]
        filtered_tokens = [t for t in alpha_tokens if not t.lower() in stop]
        return filtered_tokens
    
    def getInvertedList(self, recordNumb, tokens):
        for token in tokens:
            if (token not in self.words):
                self.words[token] = []
            self.words[token].append(recordNumb)
        

l = ListaInvertida()
l.generate("data/cf74.xml")
        
        
        
        