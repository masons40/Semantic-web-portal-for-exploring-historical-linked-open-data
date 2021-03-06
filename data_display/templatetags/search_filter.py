from django import template
import rdflib
from rdflib.graph import Graph
import json
import requests
import re
register = template.Library()
names = ['Questionnaire','Question','PaperSlipRecord','PaperSlip','Source','Multimedia','Lemma','Person']

imageSources = []
@register.simple_tag(takes_context=True)
def typeTest(context,i,arg):
    if context[i]['type'][arg] == 'uri':
        return True
    return False	
	
counter = 0
def word(string,findCharacter,secondCharacter):
    #creates a smaller word to diplay, visual use only 
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
	
@register.simple_tag(takes_context=True)
def getTitle(context, type, indexPos):

    num = int(indexPos)
    newDic = retData(context[num]) #context is a dictionary of urls(subjects) with values like "http://exploreat.adaptcentre.ie/Questionnaire/1"
    #retData will return all the related data to the subject, ie. title,label,hasAuthor etc
    try:
        for key,value in newDic.items():
            #look for the label and return it
            if value['shortname'][0] == 'label':
                newName = value['shortname'][1] 
                return newName[0:13]+'...'
    except:
        return 'no label found'
            
    return 'hello'
# function gets all the data from a given url, will create a type,value and shortname key. all keys have values of lists which contain the info from the url
def retData(stringUrl):
    #retrieves all relevant data from the parsed json url, works for all entities and is used in dataDisplay
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
    data['type'] = getType(stringUrl)
    return data;
@register.simple_tag(takes_context=True)
def getTypeForIndex(context,urlNum,num):
    #num is a boolean, context contains a dictionary of subjects 
    dic = retData(context[urlNum])
    if num:
        return dic['type'] + "/" + dic['id'] #will return a url for navigation such as Questionnaire/1 
    return dic['type'] + " " + dic['id']
	
def getType(url):
    for name in names:
        if url.find(name) != -1:
            return name
    
    return 0
	
@register.simple_tag()
def makeUrl(string):
    #creates the urls needed in the index page to view more information about the entity
    
    return '../../../' + 'data_display/infoDisplay/'+string
	
@register.simple_tag()
def rangeForIndex():
    return range(0,3)
	
@register.simple_tag(takes_context=True)
def getInfoForIndex(context,firstNum,secondNum):
    # in this case context is a dictionary of subjects containing urls.
    dic = retData(context[firstNum]) #return all information about the url ie,title label etc. firstnum is from the first range (0,10)
    val = dic[secondNum]['shortname'][1] #will return the predicate to be shown. ie, label,title etc
    return dic[secondNum]['shortname'][0] + ": " + val[0:6] + "..." #predication and object value will be returned

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
def test(url):
    #pattern matching technique to create urls for navigation to other linked entities
    pattern = re.compile(r'[a-zA-Z]*/[0-9]*')
    patternTwo = re.compile(r'http://exploreat.adaptcentre.ie/')
    matches = patternTwo.finditer(url)
    for match in matches:
        newString = url[int(match.span()[1]):len(url)]
        matchesTwo = pattern.finditer(newString)
        for m in matchesTwo:
            return '../../infoDisplay/'+newString[m.span()[0]:m.span()[1]]
    return url	
@register.simple_tag()	
def extraction(url):
    if "exploreat.adaptcentre.ie" in url or 'prismstandard' in url:
        return "";
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

#image handling 	
@register.simple_tag()	
def imagesRange():
    return range(0,len(imageSources))
	
@register.simple_tag()	
def addImageSource(source):
    imageSources.append(str(source))

@register.simple_tag()	
def imageTest(source):
    if '.jpg' in source or '.png' in source:
        return True
    else:
        return False

@register.simple_tag()	
def makeImageName():
    newStr = "image" + str(len(imageSources))
    return newStr	

@register.simple_tag()	
def makeNewImageName(num):
    newStr = "image" + str(num)
    return newStr
	
#end of images handling 

@register.simple_tag()	
def makeName(firstIndex):
    newStr = "saveIcons" + str(firstIndex)
    return newStr

@register.simple_tag()
def getSelected(selected):
    newUrl = 'http://exploreat.adaptcentre.ie/'+str(selected)+'10/1'
    context = retData(newUrl)


@register.simple_tag()
def backTen(amount, offset, type):
    if amount==10 and offset==1:
        return ''
    else:
        newAmount = int(amount)- 10
        newOffset = int(offset)- 10
    return '../../../../data_display/'+str(type)+'/'+str(newAmount)+'/'+str(newOffset)
	
@register.simple_tag()
def forwardTen(amount, offset, type):
    newOffset = int(offset)+10
    return '../../../../data_display/'+str(type)+'/'+str(amount)+'/'+str(newOffset)
	
@register.simple_tag()
def moduloTest(arg):
    if arg%2 == 0:
        return True
    else:
        return False
	
	
	
	
	
	
	
	
	