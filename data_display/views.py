import json
import requests
import datetime as dt
import rdflib
from rdflib.graph import Graph
from SPARQLWrapper import SPARQLWrapper,JSON
from . import models
from django.shortcuts import render
from collections import defaultdict
from . import forms
from django.contrib.auth.decorators import login_required
from data_display.models import changes
from django.shortcuts import get_object_or_404
from django.contrib.auth.forms import AuthenticationForm



names = ['Questionnaire','Question','PaperSlip','Source','Multimedia','PaperSlip Record','Lemma','Person']

def index(request,type=None,amount=None,offset=None):
    url2 = "http://exploreat.adaptcentre.ie/"
    
    if request.method == 'POST':
	
        try:
            #left arrow navigation is triggered
            left = request.POST['left']
            type = request.POST['type']
            amount=request.POST['amount']
            amountN = int(amount)+int(left)
            if amount==10:
                newUrl = url2 + type

                context = getAllInfo(newUrl,10,1,type)
                return render(request, 'data_display/index.html',context)
            offset=request.POST['offset']
            offsetN = int(offset)+int(left)
            newUrl = url2 + type

            context = getAllInfo(newUrl,amountN,offsetN,type)
            return render(request, 'data_display/index.html',context)
        except:
            print("using right arrow")
        try:
            #right arrow navigation is triggered
            right = request.POST['right']
            type = request.POST['type']
            amount=request.POST['amount']
            amountN = int(amount)+int(right)
            offset=request.POST['offset']
            offsetN = int(offset)+int(right)
            newUrl = url2 + type
            
            context = getAllInfo(newUrl,amount,offsetN,type)
            
            return render(request, 'data_display/index.html',context)
        except:
            print("using left arrow")
			
		
        strUrl='http://exploreat.adaptcentre.ie/'
        strUrl+=str(request.POST.get('type'))
        strUrl+='/'+str(request.POST.get('id'))
        context = retData(strUrl)
        return render(request, 'data_display/dataDisplay.html',context)
    if type != None:
        newUrl = url2 + type
        context = getAllInfo(newUrl,amount,offset,type)
        context["displayCards"] = True;
        return render(request, 'data_display/index.html',context)
       
    if request.user.is_authenticated:
        username = request.user.username
        loggedIn = True
        context = {'username':username,'loggedIn':loggedIn}
    else:
        context = {'loggedIn':False}
        form = AuthenticationForm()
        context['form']=form
		
    return render(request, 'data_display/home.html',context)
	
def search(request):
    dataset="http://localhost:3030/dboe/query"
    subject = request.POST['type']
    predicate = request.POST['select2']
    object = request.POST['val']
    
    #the query will strip the questionnaire number and replace http://localhost/oldca/fragebogen/1 in the query
    sparql = SPARQLWrapper(dataset)
    sparql.setQuery("""
	
                    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                    prefix oldcan: <https://explorations4u.acdh.oeaw.ac.at/ontology/oldcan#>
				
                    SELECT *
					from Named <http://exploreat.adaptcentre.ie/Questionnaire_graph>
                    WHERE {
					 Graph <http://exploreat.adaptcentre.ie/Questionnaire_graph>{
							?s rdf:type oldcan:""" + subject +""".
							?s """ + predicate +""" ?o .
							Filter regex(?o, \"""" + object +"""\" ,"i").
							
						}
					} 
					limit 10
                 """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    
    context = {}
    index =0;
    length = len(results['results']['bindings'])
    for i in range(0,length):
        context[i] = results['results']['bindings'][i]['s']['value'];
    
    context['range'] = range(0,length);
    return render(request, 'data_display/index.html',context)

def infoDisplay(request,type,id):
    defaultStrUrl='http://exploreat.adaptcentre.ie/'

    if request.method == 'POST':
        strUrl='http://exploreat.adaptcentre.ie/'+type+'/'+id
        strUrl+=str(request.POST.get('typeValue'))
        strUrl+='/'+str(request.POST.get('id'))
        
        context = retData(strUrl)
        return render(request, 'data_display/index.html',context)
    context = retData('http://exploreat.adaptcentre.ie/'+type+'/'+id)
    context['targetUri'] = 'http://exploreat.adaptcentre.ie/'+type+'/'+id
    return render(request, 'data_display/dataDisplay.html',context)

# function used to create single words instead of long urls	
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
   
    i=0
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
        
        if word(binding['p']['value'],'#','/') == 'label':
            data['name'] = binding['o']['value']

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
    data['form'] = forms.changeForm()
    """
        example dictionary created by retData, each bit of info from the entity will have a sub dictionary telling the user of the type and value
        ,shortnames is there for display purposes. notice how in the sub-dictionary (0) that value[0] = 'http://www.w3.org/2000/01/rdf-schema#label' this is the prediacte
        with the object value = value[1], type[0] tell us that the predicate value is a uri and the corresponding object value is a literal
    {
        'name': 'Fragebogen 2: Die Osterwoche (1)', 
        0:  {
                'type': ['uri', 'literal'], 
                'value': ['http://www.w3.org/2000/01/rdf-schema#label', 'Fragebogen 2: Die Osterwoche (1)'], 
                'shortname': ['label', 'Fragebogen 2: Die Osterwoche (1)']
            }, 
        1:  {
                'type': ['uri', 'literal'], 
                'value': ['https://explorations4u.acdh.oeaw.ac.at/ontology/oldcan#note', 'bafb2'], 
                'shortname': ['note', 'bafb2']
            }, 
        2:  {
                'type': ['uri', 'uri'], 
                'value': ['http://www.w3.org/1999/02/22-rdf-syntax-ns#type', 'https://explorations4u.acdh.oeaw.ac.at/ontology/oldcan#Questionnaire'],
                'shortname': ['type', 'Questionnaire']
            }, 
        3:  {
                'type': ['uri', 'uri'],
                'value': ['http://www.w3.org/1999/02/22-rdf-syntax-ns#type', 'https://explorations4u.acdh.oeaw.ac.at/ontology/oldcan#SystematicQuestionnaire'],
                'shortname': ['type', 'SystematicQuestionnaire']
            }, 
        4:  {
                'type': ['uri', 'literal'], 
                'value': ['https://explorations4u.acdh.oeaw.ac.at/ontology/oldcan#title', 'Fragebogen 2: Die Osterwoche (1)'],
                'shortname': ['title', 'Fragebogen 2: Die Osterwoche (1)']
            }, 
        5:  {
                'type': ['uri', 'uri'], 
                'value': ['https://explorations4u.acdh.oeaw.ac.at/ontology/oldcan#hasAuthor', 'http://exploreat.adaptcentre.ie/Person/22192'], 
                'shortname': ['hasAuthor', '22192']
            }, 
        6:  {
                'type': ['uri', 'literal'], 
                'value': ['https://explorations4u.acdh.oeaw.ac.at/ontology/oldcan#publicationYear', '1920'], 
                'shortname': ['publicationYear', '1920']
            }, 
        'id': '2', 
        'range': range(0, 7), 
        'form': <changeForm bound=False, valid=Unknown, fields=(newValue)>
	}
		form in this case will have values from forms.py (just newValue)
        range(0,7) is because the entity contained 6 piece of information
    """
    return data
	
def getAllInfo(url,amount,offset,type):
    # getAllInfo is used to gather 10 subjects of an entity. ie, the first 10 questionnaires etc. 
    newUrl = url + '/' + str(amount) + '/' + str(offset)
    # newUrl could look like https//:explo...../Questionnaire/10/1
    data={} #empty dictionary to store teh subjects we recieve
    
    response = requests.get(newUrl)
    todos = json.loads(response.text)
    results = ""
    results = todos["results"]
    bindings = todos["results"]["bindings"]
    index = 0
    # the returned JSON actually contains repetitions of the same url, so we check for duplicates with checkDataContained(which takes in the current dictionary, and the value to test for)
    for binding in bindings:
        if checkDataContained(data,binding['s']['value']) != True:
            data[index] = binding['s']['value']
            index += 1
    data['range'] = range(0,index)
    data['type'] = type
    data['amount'] = amount
    data['offset'] = offset
    #add the additional information to the dictionary such as range, offset etc. this is used in the hmtl template to display information
    """
        example of show the created dictionary would look with all the data
    {
        0: 'http://exploreat.adaptcentre.ie/Questionnaire/2', 
        1: 'http://exploreat.adaptcentre.ie/Questionnaire/3', 
        2: 'http://exploreat.adaptcentre.ie/Questionnaire/4', 
        3: 'http://exploreat.adaptcentre.ie/Questionnaire/5', 
        4: 'http://exploreat.adaptcentre.ie/Questionnaire/6', 
        5: 'http://exploreat.adaptcentre.ie/Questionnaire/7', 
        6: 'http://exploreat.adaptcentre.ie/Questionnaire/8', 
        7: 'http://exploreat.adaptcentre.ie/Questionnaire/9', 
        8: 'http://exploreat.adaptcentre.ie/Questionnaire/10', 
        9: 'http://exploreat.adaptcentre.ie/Questionnaire/11', 
        'range': range(0, 10), 
        'type': 'Questionnaire', 
        'amount': '10', 
        'offset': '1'
    }
	"""
    return data
	
def checkDataContained(data,value):
    i=0
    for k,v in data.items():
        if value == v:
            return True
            
    return False

	
#function saves the data that has been changed 		
@login_required(login_url="account:login")		
def changed(request):
   
    try:
        obj = changes.objects.get(pk=request.POST['id'])
        
        obj.oldValue = request.POST['oldValue']
        obj.attributeName = request.POST['attributeName']
        obj.targetUri = request.POST['targetUri']
        obj.newValue = request.POST['newValue']
        obj.save()
    except changes.DoesNotExist:
       
        NoldValue = request.POST['oldValue']
        NattributeName = request.POST['attributeName']
        NnewValue = request.POST['newValue']
        NtargetUri = request.POST['targetUri']
        Nid = request.POST['id']
        NuserId = request.user.id
		
        newObj = changes(id=Nid,targetUri=NtargetUri,attributeName=NattributeName,oldValue=NoldValue,newValue=NnewValue,userId=NuserId)
        newObj.save()
    return render(request,'data_display/base.html')
						

			