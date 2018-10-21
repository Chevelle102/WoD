"""
@author: U{Nines Sanguino}
@version: 0.2
@since: 02Feb2018
"""

__version__ = '0.2'
__modified__ = '02Feb2018'
__author__ = 'Nines Sanguino'
from SPARQLWrapper import SPARQLWrapper, JSON, XML, RDF
import xml.dom.minidom

def getLocalLabel (instancia):
 
 	sparqlSesame = SPARQLWrapper("http://localhost:8080/rdf4j-server/repositories/SocialNetwork",  returnFormat=JSON)
	queryString = "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX sn:  <http://ciff.curso2015/ontologies/owl/socialNetwork#> SELECT ?label WHERE { sn:" + instancia + " rdfs:label ?label }"
	sparqlSesame.setQuery(queryString)
	sparqlSesame.setReturnFormat(JSON)
	query   = sparqlSesame.query()
	results = query.convert()
	devolver = []
	for result in results["results"]["bindings"]:
		label = result["label"]["value"]
		if 'xml:lang' in result["label"]:
			lang = result["label"]["xml:lang"]
		else:
			lang = None
		print "The label: " + label
		if 'xml:lang' in result["label"]:
			print "The lang: " + lang
		devolver.append((label, lang))
	return devolver


	
def getDBpediaResource (label, lang, endpoint):

	sparqlDBPedia = SPARQLWrapper(endpoint)
	if (lang):
		# Tenemos en cuenta las rdfs:label con @lang, por ejemplo "Alicia Keys"@en
		# Aqui os dejo plantada una query para este caso de dbpedia 
		# Algunos valores llevan includo el lenguaje en el que esta expresado. Si echais un vistazo al fichero entidades.n3
		# podreis ver valores de propiedades como "Cervantes Saavedra, Miguel de"@es. Eso quiere decir que el valor de la propiedad es 
		# "Cervantes Saavedra, Miguel de" y que el lenguaje en que esta expresado es espanol. Para buscar esa misma etiqueta en repositorios remotos
		# tendreis que preguntar incluir @es en la propia SPAQRL. Os dejo un esbozo abajo
		queryString = "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> SELECT ?s WHERE { ?s rdfs:label \"" + label + "\"@" +lang + " . } "
	else:
		# Tenemos en cuenta las rdfs:label sin @lang, por ejemplo "Alicia Keys"
		# Aqui es donde se debe insertar una QUERY SPARQL similar a la que os he dejado planteada pero sin el lang
		#queryString = "" 
		queryString = "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> SELECT ?s WHERE { ?s rdfs:label \"" + label + " . }"

	
	sparqlDBPedia.setQuery(queryString)
	sparqlDBPedia.setReturnFormat(JSON)
	query   = sparqlDBPedia.query()
	results = query.convert()
	print
	for result in results["results"]["bindings"]:
		resource = result["s"]["value"]
		print "->The resource: " + resource


def getLinkedmdbResource (label, lang, endpoint):

	sparqlLinkedmdb = SPARQLWrapper(endpoint)

	if (lang):
		# Tenemos en cuenta las rdfs:label con @lang, por ejemplo "Batman"@es
		# Aqui es donde se debe insertar la QUERY SPARQL con las propieades que use LinkedMDB
		#queryString = "" 
		queryString = "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> SELECT ?s WHERE { ?s rdfs:label \"" + label + "\"@" +lang + " . } "

	else:
		# Tenemos en cuenta las rdfs:label sin @lang, por ejemplo "Batman"
		# Aqui es donde se debe insertar la QUERY SPARQL con las propieades que use LinkedMDB, pero sin el uso de lang
		#queryString = "" 
		queryString = "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> SELECT ?s WHERE { ?s rdfs:label \"" + label + "\"" "} "

	
	sparqlLinkedmdb.setQuery(queryString)
	sparqlLinkedmdb.setReturnFormat(JSON)
	query   = sparqlLinkedmdb.query()
	results = query.convert()
	print
	for result in results["results"]["bindings"]:
		resource = result["s"]["value"]
		print "->The resource: " + resource
		

def getBNEResource (label, lang, endpoint):

	sparqlBNE = SPARQLWrapper(endpoint)
	if (lang):
		# Tenemos en cuenta las rdfs:label con @lang, por ejemplo Cervantes Saavedra, Miguel de"@es
		# Aqui es donde se debe insertar la QUERY SPARQL con las propieades que use BNE
		#queryString = ""
		queryString = "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> SELECT ?s WHERE { ?s rdfs:label \"" + label + "\"@" +lang + " . } "

	else:
		# Tenemos en cuenta las rdfs:label sin @lang, por ejemplo "Cervantes Saavedra, Miguel de"
		# Aqui es donde se debe insertar la QUERY SPARQL con las propieades que use BNE, sin lang
		#queryString = ""
		queryString = "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> SELECT ?s WHERE { ?s rdfs:label \"" + label + "\""  "}"

		
	sparqlBNE.setQuery(queryString)
	sparqlBNE.setReturnFormat(JSON)
	query   = sparqlBNE.query()
	results = query.convert()
	print
	for result in results["results"]["bindings"]:
		resource = result["s"]["value"]
		print "->The resource: " + resource



if __name__ == '__main__':

	
	lista = getLocalLabel("instancia1");
	print lista
	endpoint = 'http://dbpedia.org/sparql';
	for result in lista:
		(label, lang) = result
		resource = getDBpediaResource (label, lang, endpoint);

	print "\n-----------1----------\n"

	# Cambiar/completar el "endpoint" por el sparql endopoint del dataset remoto con el que se vaya a enriquecer cada instancia local
	lista = getLocalLabel("instancia3");
	print lista
	endpoint = 'http://data.linkedmdb.org/sparql';
	for result in lista:
		(label, lang) = result
		resource = getLinkedmdbResource (label, lang, endpoint);

	print "\n------------2---------\n"

	# Cambiar/completar "endpoint" por el sparql endopoint del dataset remoto con el que se vaya a enriquecer cada instancia local
	lista = getLocalLabel("instancia4");
	print lista
	endpoint = 'http://datos.bne.es/sparql';
	for result in lista:
		(label, lang) = result
		resource = getBNEResource (label, lang, endpoint);
	

		
	print "\n------------3---------\n"

