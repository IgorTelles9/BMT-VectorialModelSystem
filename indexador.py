import csv
import math
from decimal import Decimal, getcontext
import time 
MODULE = "[INDEXADOR] "
class Indexador:
    def __init__(self, config_file):
        print(MODULE, "Iniciando...")
        self.config_file = config_file
        self.configuration()
        getcontext().prec = 5
    
    def generate(self):
        print(MODULE, "Gerando matriz termo-documento...")
        start = time.time()
        self.getInvertedList()
        print(MODULE, "Listas invertidas extraídas")
        self.getFrequencies()
        print(MODULE, "Frequencias de palavras por documento calculadas")
        self.getTermDocumentMatrix()
        self.write_results()
        end = time.time()
        print(MODULE, "Matriz termo-documento gerada com sucesso em ", self.file_to_write)
        print(MODULE, "Tempo levado: ", str(end-start), "s")

    def configuration(self):
        self.nDocs = 0
        print(MODULE, "Lendo arquivo de configuração") 
        try:
            with open(self.config_file, 'r') as file:
                for line in file:
                    line = line.strip()
                    key, value = line.split("=", 1)
                    if (key == "LEIA"):
                        self.file_to_read = value
                    elif (key == "ESCREVA"):
                        self.file_to_write = value
            print(MODULE, "Arquivo de configuração lido com sucesso!")
        except FileNotFoundError:
            print(MODULE, "ERRO: Arquivo de configuração não encontrado") 
    
    def write_results(self):
        with open(self.file_to_write, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=";")
            writer.writerow(['#'] + list(range(1, len(self.matrix[0]) + 1)))
            for i, word in enumerate(self.wordsList):
                row_data = [word] + self.matrix[i][1:]
                writer.writerow(row_data)

    def getInvertedList(self):
        self.inverted_list = {}
        with open(self.file_to_read, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            for row in reader:
                word = row[0]
                numbers_str = row[1][1:-1]
                numbers_list = [int(num) for num in numbers_str.split(',')] 
                self.inverted_list[word] = numbers_list
    
    def getTermDocumentMatrix(self):
        self.matrix = [["0.0"] * (self.nDocs + 1) for _ in range(len(self.words_freqs.keys()))]
        self.wordsList = []
        i = 0
        for word, docs in self.words_freqs.items():
            numDocs = len(docs)
            for num, freq in docs.items():
                self.matrix[i][num] = self.getTF_IDF(freq, numDocs)
            self.wordsList.append(word)
            i += 1

    def getTF_IDF(self, freq, numDocs):
        return str(freq * self.getIDF(numDocs))


    def getIDF(self, nDocsWord):
        return Decimal(math.log(Decimal(str(self.nDocs))/Decimal(str(nDocsWord))))
    
    def getFrequencies(self):
        self.words_freqs = {}
        for word, docs in self.inverted_list.items():
            self.words_freqs[word] = self.getWordFrequencies(docs)

    def getWordFrequencies(self, docs):
        maxDoc = ""
        freqs = {}
        for doc in docs:
            if doc > self.nDocs:
                self.nDocs = doc
            if not freqs:
                maxDoc = doc 
            if doc not in freqs.keys():
                freqs[doc] = 0
            freqs[doc] += 1
            if doc != maxDoc and freqs[doc] > freqs[maxDoc]:
                maxDoc = doc
        return self.normalizeFreqs(freqs, maxDoc)
        
    def normalizeFreqs(self, freqs, maxDoc):
        maxFreq = freqs[maxDoc]
        norm_freqs = {}
        for doc, freq in freqs.items():
            norm_freqs[doc] = Decimal(str(freq))/Decimal(str(maxFreq))
        return norm_freqs


# indexador = Indexador("INDEX.cfg")
# indexador.generate()
                