from xml.etree import ElementTree as ET
import csv

class ProcessadorConsultas:
    def __init__(self, config_file):
        self.config_file = config_file
        self.configuration()
        
    def configuration(self):
        config = self.readConfig()
        self.file_to_read = config["LEIA"]
        self.consultas_file = config["CONSULTAS"]
        self.esperados_file = config["ESPERADOS"]
        print(self.consultas_file)

    def readConfig(self):
        config_data = {}
        try:
            with open(self.config_file, 'r') as file:
                for line in file:
                    line = line.strip()
                    key, value = line.split("=", 1)
                    config_data[key] = value.strip()
        except FileNotFoundError:
            print("Error: File not found!")
        return config_data
    
    def getConsultas(self):
        print(self.file_to_read)
        try:
            self.root = ET.parse(self.file_to_read).getroot()
            self.getConsultasTable()
            self.save_csv(self.consultasTable, self.consultas_file)
        except:
            print("ERROR")
    
    def getEsperados(self):
        try:
            self.root = ET.parse(self.file_to_read).getroot()
            self.getEsperadosTable()
            self.save_csv(self.esperadosTable, self.esperados_file)
        except:
            print("ERROR1")
        
    def getConsultasTable(self):
        self.getQueryNumbers()
        self.getTexts()
        self.consultasTable = []
        for i in range(len(self.queryNumbers)):
            self.consultasTable.append([self.queryNumbers[i],self.texts[i]])
        self.consultasTable.insert(0, ["QueryNumber", "QueryText"])
        
    def getEsperadosTable(self):
        self.getQueryNumbers()
        self.getResults()
        self.getDocNumbersAndVotes()
        self.insertQueryNumber()
        self.esperadosTable.insert(0, ["QueryNumber", "DocNumber", "DocVotes"])
    
    def getDocNumbersAndVotes(self):
        self.esperadosTable = []
        for item in self.root.findall("QUERY/Records/Item"):
            docNumber = int(item.text)
            docVotes = self.getVotes(item.get("score"))
            self.esperadosTable.append([docNumber, docVotes])
            
    def getVotes(self, score):
        votes = 0
        for x in score:
            if int(x) > 0:
                votes+=1
        return votes
    
    def getResults(self):
        self.results = []
        for result in self.root.findall("QUERY/Results"):
            self.results.append(int(result.text))
             
    def insertQueryNumber(self):
        lineCounter = 0
        for i in range(len(self.queryNumbers)):
            for j in range(self.results[i]):   
                self.esperadosTable[lineCounter].insert(0, self.queryNumbers[i])
                lineCounter+=1
            
                
    def getQueryNumbers(self):
        self.queryNumbers = []
        for number in self.root.findall("QUERY/QueryNumber"):
            numberText = number.text 
            self.queryNumbers.append(int(numberText))
    
    def getTexts(self):
        self.texts = []
        for text in self.root.findall("QUERY/QueryText"):
            rawText = text.text
            textMultipleSpaces = rawText.replace("\n", "")
            cleanText = " ".join(textMultipleSpaces.split())
            self.texts.append(cleanText)
                

    def save_csv(self, data, file_to_save):
        with open(file_to_save, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')
            writer.writerows(data)

processador = ProcessadorConsultas("config.txt")
processador.getConsultas()
processador.getEsperados()

    
