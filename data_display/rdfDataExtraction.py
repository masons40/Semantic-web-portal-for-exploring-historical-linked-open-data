import rdflib
from rdflib.graph import Graph

def extraction(url):
    g = Graph()
    g.parse(url)
    
    for s,p,o in g:
        print("subject",s)
        print("predicate",p)
        print("object",o)
        print()
    
		
extraction("https://expoloreations4u.acdh.oeaw.ac.at/ontology/oldcan#Questionnaire")