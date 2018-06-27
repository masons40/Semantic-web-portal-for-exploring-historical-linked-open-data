from django.urls import path
from . import views

app_name = 'data_display'
urlpatterns = [
    path('', views.index, name='index'),
    path('<type>', views.index, name='index'),
    path('edit', views.edit, name='edit'),
	path('changed', views.changed,name='changed'),
	path('infoDisplay/<type>/<id>', views.infoDisplay,name='infoDisplay')
]