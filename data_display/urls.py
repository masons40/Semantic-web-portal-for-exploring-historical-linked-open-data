from django.urls import path
from . import views

app_name = 'data_display'
urlpatterns = [
    path('', views.index, name='index'),
]