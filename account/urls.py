from . import views
from django.conf.urls import url
 
 
app_name = 'account'

urlpatterns = [
    url(r'^signup/',views.signup_view,name='signup'),
    url(r'^login/',views.login_view,name='login'),
	url(r'^logout/',views.logout_view,name='logout')
]