import json
import requests

from django.shortcuts import render
from collections import defaultdict
from data_display.forms import retForm


def index(request):
 
    context = retData("http://exploreat.adaptcentre.ie/Source/1")

    return render(request, 'data_display/index.html',context)
	
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

def get(request):
    form = retForm()
    print(request.get)
    return render(request,'data_display/index.html',{'form':form})

def post(request):
    print(request.post)
    form = retForm(request.POST)
    if form.is_valid():
	    text = form.cleaned_data['post']
	
    print("hello")
    print(text)
    return render(request, 'data_display/index.html',context)
	
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

    return data;
			
			
			
def edit(request):
    context = retData("http://exploreat.adaptcentre.ie/Source/1")

    return render(request, 'data_display/edit.html',context)
			
			
			
			