import rdflib
from rdflib.graph import Graph

def extraction(url):
    g = Graph()
    g.parse(url)
	
    qres = g.query(
    """
	   SELECT DISTINCT ?obj
       WHERE {<"""+
        url + """> rdfs:comment ?obj 
       }
    """
    )
    comment=''
    for res in qres:
        comment+=str(res)
    return comment

extraction("https://explorations4u.acdh.oeaw.ac.at/ontology/oldcan#note")