import json
import requests
import datetime as dt
from . import models
from django.shortcuts import render
from collections import defaultdict
from . import forms
from django.contrib.auth.decorators import login_required
from data_display.models import changes
from django.shortcuts import get_object_or_404



names = ['Questionnaire','Question','PaperSlip','Source','Multimedia','PaperSlip Record','Lemma','Person']
#index currently works for everything except Question
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
            
            context = getAllInfo(newUrl,amountN,offsetN,type)
            
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
        return render(request, 'data_display/index.html',context)
       
    
    return render(request, 'data_display/base.html')
	
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
    
    return data;
	
def getAllInfo(url,amount,offset,type):
    newUrl = url + '/' + str(amount) + '/' + str(offset)
    
    data={}
    
    response = requests.get(newUrl)
    todos = json.loads(response.text)
    results = ""
    results = todos["results"]
    bindings = todos["results"]["bindings"]
    endRange=0
    index = 0
  
    for binding in bindings:
        if checkDataContained(data,binding['s']['value']) != True:
            data[index] = binding['s']['value']
            index += 1
            endRange+=1
    data['range'] = range(int(offset)-1,endRange)
    data['type'] = type
    data['amount'] = amount
    data['offset'] = offset
    print("DATA:",data)
    return data
	
def checkDataContained(data,value):
    i=0;
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
						

			