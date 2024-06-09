from processador_consultas import ProcessadorConsultas
from lista_invertida import ListaInvertida
from indexador import Indexador
from buscador import Buscador
import metricas

with open("BUSCA.cfg", "r") as file:
    stemmer = file.readline().strip("\n")
    if stemmer == "STEMMER":
        print("Rodando com Stemmer")
    else:
        print("Rodando sem Stemmer")

processador = ProcessadorConsultas("PC.cfg")
processador.getConsultas()
processador.getEsperados()

l = ListaInvertida("GLI.cfg")
l.generate()

indexador = Indexador("INDEX.cfg")
indexador.generate()

buscador = Buscador("BUSCA.cfg")
buscador.generate()

print("Gerando métricas...")
metricas.generate(stemmer)