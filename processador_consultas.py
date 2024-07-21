from xml.etree import ElementTree as ET
import csv
MODULO = "[PROCESSADOR DE CONSULTAS] "

class ProcessadorConsultas:
    def __init__(self, config_file):
        print(MODULO, "Iniciando...")
        self.config_file = config_file
        self.configuration()
        
    def configuration(self):
        config = self.readConfig()
        self.file_to_read = config["LEIA"]
        self.consultas_file = config["CONSULTAS"]
        self.esperados_file = config["ESPERADOS"]

    def readConfig(self):
        config_data = {}
        try:
            print(MODULO, "Lendo arquivo de configuração...")
            with open(self.config_file, 'r') as file:
                for line in file:
                    line = line.strip()
                    key, value = line.split("=", 1)
                    config_data[key] = value.strip()
            print(MODULO, "Arquivo de configuração lido com sucesso")
        except FileNotFoundError:
            print(MODULO, "Arquivo de configuração não encontrado")
        return config_data
    
    def getConsultas(self):
        try:
            print(MODULO, "Obtendo consultas...")
            self.root = ET.parse(self.file_to_read).getroot()
            self.getConsultasTable()
            self.save_csv(self.consultasTable, self.consultas_file)
            print(MODULO, "Consultas salvas no arquivo ", self.consultas_file) 
        except:
            print(MODULO, "Erro ao obter consultas")
    
    def getEsperados(self):
        try:
            print(MODULO, "Obtendo esperados...")
            xml = ET.parse(self.file_to_read).getroot()
            self.getEsperadosTable(xml)
            self.save_csv(self.esperadosTable, self.esperados_file)
            print(MODULO, "Esperados salvos no arquivo ", self.esperados_file)
        except:
            print(MODULO, "Erro ao obter esperados")
        
    def getConsultasTable(self):
        self.getQueryNumbers()
        self.getTexts()
        self.consultasTable = []
        for i in range(len(self.queryNumbers)):
            self.consultasTable.append([self.queryNumbers[i],self.texts[i]])
        self.consultasTable.insert(0, ["QueryNumber", "QueryText"])
        
    def getEsperadosTable(self, xml):
        self.esperadosTable = []
        for query in xml.findall('QUERY'):
            query_number = int(query.find('QueryNumber').text)
            
            for item in query.find('Records').findall('Item'):
                document_number = int(item.text)
                document_votes = sum(int(digit) for digit in item.attrib['score'])
                self.esperadosTable.append([query_number, document_number, document_votes])
        self.esperadosTable.insert(0, ["QueryNumber", "DocNumber", "DocVotes"])
         
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

    
