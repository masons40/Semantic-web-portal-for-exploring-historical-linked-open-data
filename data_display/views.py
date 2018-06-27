import json
import requests
import datetime as dt
from . import models
from django.shortcuts import render
from collections import defaultdict
from . import forms
from django.contrib.auth.decorators import login_required

import rdflib
from rdflib.graph import Graph

url = "http://exploreat.adaptcentre.ie/"
names = ['Questionnaire','Question','PaperSlip','Source','Multimedia','PaperSlip Record','Lemma','Person']
#index currently works for everything except Question
def index(request,type=None):
    if request.method == 'POST':
        strUrl='http://exploreat.adaptcentre.ie/'
        strUrl+=str(request.POST.get('typeValue'))
        strUrl+='/'+str(request.POST.get('id'))
        context = retData(strUrl)
        return render(request, 'data_display/index.html',context)
    if type != None:
        newUrl = url + type
        print(newUrl)
        #context = getAllInfo(newUrl)
        #return render(request, 'data_display/index.html',context)
       
    
    return render(request, 'data_display/base.html')
	
def infoDisplay(request,type,id):
    if request.method == 'POST':
        strUrl='http://exploreat.adaptcentre.ie/'+type+'/'+id
        strUrl+=str(request.POST.get('typeValue'))
        strUrl+='/'+str(request.POST.get('id'))
        context = retData(strUrl)
        return render(request, 'data_display/index.html',context)
    context = retData('http://exploreat.adaptcentre.ie/'+type+'/'+id)

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
    i=0;
    type=[]
    value=[]
    shortname=[]
    #target=0
    for binding in bindings:
        type.append(binding['p']['type'])
        #if binding['p']['type'] == 'uri':
            #iname = 'info'+word(binding['p']['value'],'#','/')
            #data['iname'] = getInfo(binding['p']['value'])
        shortname.append(word(binding['p']['value'],'#','/'))
        value.append(binding['p']['value'])
		
        #if binding['o']['type'] == 'uri':
            #iname = 'info'+word(binding['o']['value'],'#','/')
            #data['iname'] = getInfo(binding['o']['value'])
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
    data['form'] = forms.changeForm()

    return data;
			

#function to create the edit page	
@login_required(login_url="account:login")	
def edit(request):
    
    context = retData(url)

    return render(request, 'data_display/edit.html',context)
	

def getAllInfo(url):

    data={}
    response = requests.get(url)
    todos = json.loads(response.text)
    i=0
    index = 0
    for i in range(0,len(todos)):
        if checkDataContained(data,todos[i]['s']['value']) != True:
            data[index] = todos[i]['s']['value']
            index += 1
			
    return data
	
	
def checkDataContained(data,value):
    i=0;
    for k,v in data.items():
        if value == v:
            return True
            
    return False

	
#function saves the data that has been changed 			
def changed(request):
    if request.method == 'POST':
        form = forms.changeForm(request.POST)
        if form.is_valid():
            currentChange = form.save(commit=False)
            currentChange.userId = request.user.id
            currentChange.save()
    context = retData('http://exploreat.adaptcentre.ie/Questionnaire/1')
        
    return render(request,'data_display/index.html',context)
						
	
def getInfo(urlData):

    g = Graph()
    g.parse(urlData)
    subject = rdflib.term.URIRef(urlData)
    qres = g.query(
    """
	   SELECT DISTINCT ?obj
       WHERE {
          ?subject rdfs:comment ?obj 
       }
    """
    )
    print('%s'%qres)
    return 789	
			
			
			
			
			
			
			
			