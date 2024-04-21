#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 20 15:29:04 2024

@author: igort
"""
import math
import time 
import csv
MODULE = "[BUSCADOR] "
import nltk
nltk.download('stopwords')
nltk.download('punkt')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
stop = stopwords.words("english")

class Buscador: 
    def __init__(self, config_file):
        print(MODULE, "Iniciando...")
        self.config_file = config_file
        self.configuration()

    def configuration(self):
        print(MODULE, "Lendo arquivo de configuração") 
        try:
            with open(self.config_file, 'r') as file:
                for line in file:
                    line = line.strip()
                    key, value = line.split("=", 1)
                    if (key == "MODELO"):
                        self.model_file = value
                    elif (key == "CONSULTAS"):
                        self.query_file = value
                    elif (key == "RESULTADOS"):
                        self.file_to_write = value
            print(MODULE, "Arquivo de configuração lido com sucesso!")
        except FileNotFoundError:
            print(MODULE, "ERRO: Arquivo de configuração não encontrado")  

    def generate(self):
        print(MODULE, "Obtendo matriz termo-documento")
        self.getTermDocumentMatrix()
        print(MODULE, "Obtendo consultas")
        self.getQueries()
        print(MODULE, "Iniciando buscas...")
        start = time.time()
        self.searchAll()
        end = time.time()
        print(MODULE, "Buscas realizadas com sucesso. ")
        print(MODULE, "Tempo levado: " ,str(end-start), "s")
        self.write_results()
        print(MODULE, "Resultados salvos no arquivo ", self.file_to_write)

    def write_results(self):
        with open(self.file_to_write, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=";")
            for queryNumber, result in self.results.items():
                for r in result:
                    row_data = [queryNumber] + [r]
                    writer.writerow(row_data)
    
    def getTermDocumentMatrix(self):
        self.model = {}
        with open(self.model_file, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            for row in reader:
                if row[0] == "#":
                    self.nDocs = int(row[-1]) -1
                    continue
                word = row[0]
                weights_str = row[1:]
                weights = [float(w) for w in weights_str] 
                # Remember that index + 1 = DocNum
                self.model[word] = weights 
    
    def getQueries(self):
        self.queries = []
        with open(self.query_file, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            for row in reader:
                if row[0] == "QueryNumber":
                    continue
                # Remember that index + 1 = QueryNumber
                self.queries.append(row[1])
    
    def searchAll(self):
        self.results = {}
        for index, query in enumerate(self.queries):
            queryNum = str(index + 1)
            dists, ranks = self.search(query)
            self.results[queryNum] = []
            for i in range(len(dists)):
                r = [ranks[i], i+1, float("%.4f"%dists[i])]
                self.results[queryNum].append(r)
            
    def search(self, query):
        dot_product = [0.0]*self.nDocs
        euclidian = [0.0]*self.nDocs
        distances = [0.0]*self.nDocs

        tokens = self.getTokensFromQuery(query)
        q_vector = math.sqrt(len(tokens))

        # get weights
        for token in tokens:
            for i in range(self.nDocs):
                if token in self.model.keys():
                    weight = self.model[token][i]
                    if weight > 0:
                        dot_product[i] += weight
                        euclidian[i] += weight ** 2
                
        # Euclidian norm calc
        euclidian = [math.sqrt(d) for d in euclidian]
        
        # distances calc
        for i in range(self.nDocs):
            if euclidian[i] > 0:
                distances[i] = float((dot_product[i] / (euclidian[i] * q_vector) ))

        positions = self.getRanks(distances)
        return (distances, positions)

    def getRanks(self, distances):
        ranked_distances = sorted(distances, reverse=True)
        positions = []
        for dist in distances:
            index = ranked_distances.index(dist)
            positions.append(index)
            ranked_distances[index] = -1
        return positions

    def getTokensFromQuery(self, query):
        tokens = word_tokenize(query)
        alpha_tokens = [token for token in tokens if token.isalpha()]
        filtered_tokens = [t.upper() for t in alpha_tokens if not t.lower() in stop]
        return filtered_tokens

buscador = Buscador("BUSCA.cfg")
buscador.generate()