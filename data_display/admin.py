from django.contrib import admin
from .models import Type,Question,Questionnaire

# Register your models here.
admin.site.register(Type)
admin.site.register(Question)
admin.site.register(Questionnaire)