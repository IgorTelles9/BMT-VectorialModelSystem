from processador_consultas import ProcessadorConsultas
from lista_invertida import ListaInvertida
from indexador import Indexador
from buscador import Buscador

stemmer = False 
stemmerInput = input("Deseja rodar com Stemmer de Porter? (s ou n)\n")
if stemmerInput == "s":
    stemmer = True

stemmerPrint = "LIGADO" if stemmer else "DESLIGADO"

print("Rodando com Stemmer " + stemmerPrint)
processador = ProcessadorConsultas("PC.cfg")
processador.getConsultas()
processador.getEsperados()

l = ListaInvertida("GLI.cfg", stemmer)
l.generate()

indexador = Indexador("INDEX.cfg")
indexador.generate()

buscador = Buscador("BUSCA.cfg", stemmer)
buscador.generate()