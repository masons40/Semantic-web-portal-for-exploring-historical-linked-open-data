import json
import requests
import datetime as dt
from . import models
from django.shortcuts import render
from collections import defaultdict
from . import forms
from django.contrib.auth.decorators import login_required
from data_display.models import changes


import rdflib
from rdflib.graph import Graph

url = "http://exploreat.adaptcentre.ie/Questionnaire/1"
names = ['Questionnaire','Question','PaperSlip','Source','Multimedia','PaperSlip Record','Lemma','Person']
#index currently works for everything except Question
def index(request,type=None,amount=None,offset=None):
    url2 = "http://exploreat.adaptcentre.ie/"
    
    if request.method == 'POST':
        strUrl='http://exploreat.adaptcentre.ie/'
        strUrl+=str(request.POST.get('type'))
        strUrl+='/'+str(request.POST.get('id'))
        print(strUrl)
        context = retData(strUrl)
        return render(request, 'data_display/dataDisplay.html',context)
    if type != None:
        newUrl = url2 + type

        context = getAllInfo(newUrl,amount,offset)
        return render(request, 'data_display/index.html',context)
       
    
    return render(request, 'data_display/base.html')
	
def infoDisplay(request,type,id):
    defaultStrUrl='http://exploreat.adaptcentre.ie/'

    if request.method == 'POST':
        strUrl='http://exploreat.adaptcentre.ie/'+type+'/'+id
        strUrl+=str(request.POST.get('typeValue'))
        strUrl+='/'+str(request.POST.get('id'))
        print(strUrl)
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
    data['form'] = forms.changeForm()

    return data;
	
def getAllInfo(url,amount,offset):
    newUrl = url + '/' + str(amount) + '/' + str(offset)
    
    data={}
  
    response = requests.get(newUrl)
    todos = json.loads(response.text)
    results = ""
    results = todos["results"]
    bindings = todos["results"]["bindings"]
    
    index = 0
    
    for binding in bindings:
        if checkDataContained(data,binding['s']['value']) != True:
            data[index] = binding['s']['value']
            index += 1
    
    data['range'] = range(int(offset)-1,index)

    return data
	
"""
def getInfoById(url):

    data={}
    responseList=[]
    for i in range(1,10):
        response = requests.get(url+'/'+str(i))
        responseList.append(response.text)
    print(responseList)
    
	todos = json.loads(responseList)
    i=0
    index = 0
    
	for url in 
	
    for i in range(0,len(todos)):
        if checkDataContained(data,todos[i]['s']['value']) != True:
            data[index] = todos[i]['s']['value']
            index += 1
	
    return data
"""
	
def checkDataContained(data,value):
    i=0;
    for k,v in data.items():
        if value == v:
            return True
            
    return False

	
#function saves the data that has been changed 		
@login_required(login_url="account:login")		
def changed(request,id):
    print(request.POST['oldValue'])
    for key,value in request.POST.items():
        print('Key: %s' % (key) ) 
        # print(f'Key: {key}') in Python 3.6
        print('Value %s' % (value) )
    """
    form = forms.changeForm(request.POST)
    if form.is_valid():
        print('worked')
    else:
        print("not working")
    form.save()
    """
    return render(request,'data_display/base.html')
						
	
def getInfo(urlData):
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
			
			
			
			
			
			
			
			