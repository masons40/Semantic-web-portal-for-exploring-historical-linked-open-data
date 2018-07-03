from django import template
import rdflib
from rdflib.graph import Graph
import json
import requests

register = template.Library()
names = ['Questionnaire','Question','PaperSlip','Source','Multimedia','PaperSlip Record','Lemma','Person']
@register.simple_tag(takes_context=True)
def typeTest(context,i,arg):
    if context[i]['type'][arg] == 'uri':
        return True
    return False	
	
counter = 0
def word(string,findCharacter,secondCharacter):
    if string.rfind(findCharacter) == -1:
        position = string.rfind(secondCharacter)
    else:
        position = string.rfind(findCharacter)
    position += 1
    if position == -1:
        return string
    return string[position:len(string)]
	
def findName(stringUrl):
    position = stringUrl.rfind('/')
    return stringUrl[position+1:len(stringUrl)]
	
# function gets all the data from a given url, will create a type,value and shortname key. all keys have values of lists which contain the info from the url
def retData(stringUrl):
   
    data={}
    response = requests.get(stringUrl)
    todos = json.loads(response.text)
    results = ""
    results = todos["results"]
    bindings = todos["results"]["bindings"]
    i=0;
    type=[]
    value=[]
    shortname=[]
    for binding in bindings:
        type.append(binding['p']['type'])
        shortname.append(word(binding['p']['value'],'#','/'))
        value.append(binding['p']['value'])
		
        type.append(binding['o']['type'])
        value.append(binding['o']['value'])
        shortname.append(word(binding['o']['value'],'#','/'))
        
        if word(binding['o']['value'],'#','/') in names:
            data['name'] = word(binding['o']['value'],'#','/')

        data[i] = {
                'type':type,
			    'value':value,
			    'shortname':shortname
            }
        
        i+=1
        type=[]
        value=[]
        shortname=[]
	
    data['id'] = findName(stringUrl)
    data['range'] = range(0,len(data)-2)
    #data['form'] = forms.changeForm()
    data['type'] = getType(stringUrl)
    return data;
@register.simple_tag(takes_context=True)
def getTypeForIndex(context,urlNum,num):
    dic = retData(context[urlNum])
    if num:
        return dic['type'] + "/" + dic['id']
    return dic['type'] + " " + dic['id']
	
def getType(url):
    for name in names:
        if url.find(name) != -1:
            return name
    
    return 0
	
@register.simple_tag()
def makeUrl(string):
    return '../../' + 'infoDisplay/'+string
	
@register.simple_tag()
def rangeForIndex():
    return range(0,3)
	
@register.simple_tag(takes_context=True)
def getInfoForIndex(context,firstNum,secondNum):
    dic = retData(context[firstNum])
    val = dic[secondNum]['shortname'][1]
    return dic[secondNum]['shortname'][0] + ": " + val[0:9] + "..."

@register.simple_tag()	
def getQuestions():
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
    #PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    #PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    #prefix oldcan: <https://explorations4u.acdh.oeaw.ac.at/ontology/oldcan#>
    """
    SELECT ?question
    from <http://exploreat.adaptcentre.ie/Questionnaire_graph>
    from <http://exploreat.adaptcentre.ie/Question_graph>
    WHERE {
        ?question oldcan:isQuestionOf <http://exploreat.adaptcentre.ie/Questionnaire/10>. 
    }
	"""
	
	
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
    
    length = 0
    for key in context:
        length+=1
		
    
    return range(0,length)

@register.simple_tag(takes_context=True)
def getListLength(context):
    return range(0,2)

@register.simple_tag()	
def extraction(url):
    if 'w3' in url:
        return url
	
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
        comment+=str(res[0])
        
    return comment
	
	
@register.simple_tag(takes_context=True)
def getRange(context,startNum):
    return range(0,10)
    """
    if startNum == 0:
        return range(0,5)
    else:
        return range(5,10)
    """