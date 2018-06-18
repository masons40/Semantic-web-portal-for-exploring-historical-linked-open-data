from django import template

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
	
   