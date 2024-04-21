import csv
from decimal import Decimal, getcontext
W = "PSEUDOMONAS"
class Indexador:
    def __init__(self, config_file):
        self.config_file = config_file
        self.configuration()
        getcontext().prec = 5
    
    def generate(self):
        self.getInvertedList()
        self.getFrequencies()

    def configuration(self):
        try:
            with open(self.config_file, 'r') as file:
                for line in file:
                    line = line.strip()
                    key, value = line.split("=", 1)
                    if (key == "LEIA"):
                        self.file_to_read = value
                    elif (key == "ESCREVA"):
                        self.file_to_write = value
                        
        except FileNotFoundError:
            print("Error: File not found!") 

    def getInvertedList(self):
        self.inverted_list = {}
        words = []
        with open(self.file_to_read, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            for row in reader:
                word = row[0]
                numbers_str = row[1][1:-1]
                numbers_list = [int(num) for num in numbers_str.split(',')] 
                self.inverted_list[word] = numbers_list

    
    def getFrequencies(self):
        self.words_freqs = {}
        for word, docs in self.inverted_list.items():
            self.words_freqs[word] = self.getWordFrequencies(docs)

    def getWordFrequencies(self, docs):
        maxDoc = ""
        freqs = {}
        for doc in docs:
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


indexador = Indexador("INDEX.cfg")
indexador.generate()
                