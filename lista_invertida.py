# -*- coding: utf-8 -*-
from xml.etree import ElementTree as ET
import csv
import nltk
nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import time
from nltk.stem import PorterStemmer
stemmer = PorterStemmer()

stop = stopwords.words("english")

MODULE = "[LISTA INVERTIDA] "

class ListaInvertida:
    
    def __init__(self, config_file):
        print(MODULE, "Iniciando...") 
        self.words = {}
        self.config_file = config_file
        self.configuration()
        self.isStemming = False 

    def configuration(self):
        self.files_to_read = []
        print(MODULE, "Lendo arquivo de configuração") 
        try:
            with open(self.config_file, 'r') as file:
                for i,line in enumerate(file):
                    if (i > 0):
                        line = line.strip()
                        key, value = line.split("=", 1)
                        if (key == "LEIA"):
                            self.files_to_read.append(value)
                        elif (key == "ESCREVA"):
                            self.file_to_write = value
                    else:
                        self.isStemming = False if line == "NOSTEMMER" else True
            print(MODULE, "Arquivo de configuração lido com sucesso!")
        except FileNotFoundError:
            print(MODULE, "ERRO: Arquivo de configuração não encontrado") 
        
        
        
    def generate(self):
        print(MODULE, "Gerando lista invertida...")
        start = time.time()
        for file in self.files_to_read:
            self.generateOne(file)
        self.write_results()
        end = time.time()
        print(MODULE, "Lista invertida gerada com sucesso em ", self.file_to_write)
        print(MODULE, "Tempo levado: ", str(end-start), "s")
        
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
        filtered_tokens = [t.upper() for t in alpha_tokens if not t.lower() in stop]
        if self.isStemming: 
           return [stemmer.stem(token) for token in filtered_tokens]
        return filtered_tokens
    
    def getInvertedList(self, recordNumb, tokens):
        for token in tokens:
            if (token not in self.words.keys()):
                self.words[token] = []
            self.words[token].append(recordNumb)
    
    def write_results(self):
        with open(self.file_to_write, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')
            for key, value in self.words.items():
                writer.writerow([key.upper(), str(value)]) 
        

# l = ListaInvertida("GLI.cfg")
# l.generate()
        
        
        
        