from xml.etree import ElementTree as ET
import csv

class ProcessadorConsultas:
    def __init__(self, file_to_read):
        self.file_to_read = file_to_read
    
    def getConsultas(self):
        try:
            self.root = ET.parse(self.file_to_read).getroot()
            self.getConsultasTable()
            self.save_csv(self.consultasTable, "test.csv")
        except:
            print("ERROR")
    
    def getEsperados(self):
        try:
            self.root = ET.parse(self.file_to_read).getroot()
            self.getEsperadosTable()
            self.save_csv(self.esperadosTable, "test1.csv")
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
        print(1)
        self.getQueryNumbers()
        print(2)
        self.getResults()
        self.getDocNumbersAndVotes()
        print(3)
        self.insertQueryNumber()
        print(4)
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
            #print(lineCounter)
                
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

processador = ProcessadorConsultas("data/cfquery.xml")
processador.getEsperados()

    
