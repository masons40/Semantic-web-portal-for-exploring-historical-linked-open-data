import json
import requests

def getAllInfo(url):

    data={}
    response = requests.get(url)
    todos = json.loads(response.text)
    results = ""
    #print(todos)
    bindings = todos[0]['s']['value']
    i=0
    index = 0
    type=[]
    value=[]
    dict = {}
    shortname=[]
    print(bindings)
    for i in range(0,len(todos)):
        if checkDataContained(data,todos[i]['s']['value']) != True:
            data[index] = todos[i]['s']['value']
            index += 1
        else:
            type.append(todos[i]['p']['type'])
            type.append(todos[i]['o']['type'])
            value.append(todos[i]['p']['value'])
            value.append(todos[i]['o']['value'])
			
    return data
	
	
def checkDataContained(data,value):
    i=0;
    for k,v in data.items():
        for key,val in v.items():
            if value == val:
                return True
            
    return False
		
getAllInfo("http://exploreat.adaptcentre.ie/Questionnaire")