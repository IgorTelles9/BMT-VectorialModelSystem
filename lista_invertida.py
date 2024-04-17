# -*- coding: utf-8 -*-
from xml.etree import ElementTree as ET
import csv
import nltk
nltk.download('stopwords')
nltk.download('punkt')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

stop = stopwords.words("english")

class ListaInvertida:
    
    def __init__(self, config_file):
        self.words = {}
        self.config_file = config_file
        self.configuration()
    
    def configuration(self):
        self.files_to_read = []
        try:
            with open(self.config_file, 'r') as file:
                for line in file:
                    line = line.strip()
                    key, value = line.split("=", 1)
                    if (key == "LEIA"):
                        self.files_to_read.append(value)
                    elif (key == "ESCREVA"):
                        self.file_to_write = value
                        
        except FileNotFoundError:
            print("Error: File not found!")  
        
        
        
    def generate(self):
        for file in self.files_to_read:
            self.generateOne(file)
        self.write_results()
        
    def generateOne(self, file_to_read):
        root = ET.parse(file_to_read).getroot()
        records = self.getTokensByRecord(root)
        for key, value in records.items():
            self.getInvertedList(key, value)
    
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
    
    def write_results(self):
        with open(self.file_to_write, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')
            for key, value in self.words.items():
                writer.writerow([key.upper(), str(value)]) 
        

l = ListaInvertida("GLI.cfg")
l.generate()
        
        
        
        