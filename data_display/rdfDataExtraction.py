import rdflib
from rdflib.graph import Graph

def extraction(url):
    g = Graph()
    g.parse(url)
    subject = rdflib.term.URIRef(url)
    qres = g.query(
    """
	   SELECT DISTINCT ?obj
       WHERE {
          ?subject rdfs:comment ?obj 
       }
    """
    )
		
    for res in qres:
        print("%s"%res)

extraction("https://expoloreations4u.acdh.oeaw.ac.at/ontology/oldcan#title")