from django.urls import path
from . import views

app_name = 'data_display'
urlpatterns = [
    path('', views.index, name='index'),
	path('changed/<id>', views.changed,name='changed'),
	path('infoDisplay/<type>/<id>', views.infoDisplay,name='infoDisplay'),
    path('<type>/<amount>/<offset>', views.index, name='index')
]