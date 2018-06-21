import json
import requests
import datetime as dt
from . import models
from django.shortcuts import render
from collections import defaultdict
from . import forms
from django.contrib.auth.decorators import login_required

url = "http://exploreat.adaptcentre.ie/Lemma/1"

#index currently works for everything except Question
def index(request):
    if request.method == 'POST':
        strUrl='http://exploreat.adaptcentre.ie/'
        strUrl+=str(request.POST.get('typeValue'))
        strUrl+='/'+str(request.POST.get('id'))
        context = retData(strUrl)
        return render(request, 'data_display/index.html',context)
    context = retData(url)

    return render(request, 'data_display/index.html',context)

# function used to create single words instead of long urls	
def word(string,findCharacter,secondCharacter):
    char_position = 0
    i=0
  
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
    target=0
    for binding in bindings:
        type.append(binding['p']['type'])
        type.append(binding['o']['type'])
        value.append(binding['p']['value'])
        value.append(binding['o']['value'])
        shortname.append(word(binding['p']['value'],'#','/'))
        shortname.append(word(binding['o']['value'],'#','/'))
		
        if target < 1:
            data['name'] = word(binding['o']['value'],'#','/')
            target+=1

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
			
#function saves the data that has been changed 			
def changed(request):
    if request.method == 'POST':
        form = forms.changeForm(request.POST)
        if form.is_valid():
            currentChange = form.save(commit=False)
            currentChange.userId = request.user.id
            currentChange.save()
    context = retData(url)
        
    return render(request,'data_display/index.html',context)
			