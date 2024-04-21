from processador_consultas import ProcessadorConsultas
from lista_invertida import ListaInvertida
from indexador import Indexador
from buscador import Buscador

processador = ProcessadorConsultas("PC.cfg")
processador.getConsultas()
processador.getEsperados()

l = ListaInvertida("GLI.cfg")
l.generate()

indexador = Indexador("INDEX.cfg")
indexador.generate()

buscador = Buscador("BUSCA.cfg")
buscador.generate()