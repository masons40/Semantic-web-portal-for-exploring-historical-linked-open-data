import rdflib


def test():
    g = rdflib.Graph()
    g.parse("http://www.w3.org/People/Berners-Lee/card.rdf")

    qres = g.query(
        """SELECT DISTINCT ?aname ?bname
            WHERE {
                ?a foaf:knows ?b .
                ?a foaf:name ?aname .
                ?b foaf:name ?bname .
            }"""
	)

    for row in qres:
        print("%s" % row)
		

test()