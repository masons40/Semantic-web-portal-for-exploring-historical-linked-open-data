from django import template
import rdflib
from rdflib.graph import Graph
register = template.Library()

@register.simple_tag(takes_context=True)
def typeTest(context,i,arg):
    if context[i]['type'][arg] == 'uri':
        return True
    return False	
	
@register.simple_tag(takes_context=True)	
def getData(context,i,word,arg):
    return context[i][word][arg]

@register.simple_tag(takes_context=True)	
def getName(context,i):
    return displayShortName(context[i],'/')

def displayShortName(string,findCharacter):
    position = string.rfind(findCharacter)
    position += 1
    if position == -1:
        return string
    return string[position:len(string)]
	
	
@register.simple_tag(takes_context=True)	
def getLength(context):
    print(context)
    length = 0
    for key in context:
        length+=1
		
    print(length)
    return range(0,length)

@register.simple_tag(takes_context=True)
def getListLength(context):
    return range(0,2)

@register.simple_tag()	
def getInfo(urlData):

    g = Graph()
    print(urlData)
    #g.parse(urlData)
    #subject = rdflib.term.URIRef(urlData)
    qres = g.query(
    """
	   SELECT DISTINCT ?obj
       WHERE {
          ?subject rdfs:comment ?obj 
       }
    """
    )
		
    return 789
	
	
@register.simple_tag(takes_context=True)
def getRange(context,boolForExtra,startNum):
    
    return range(startNum,5)