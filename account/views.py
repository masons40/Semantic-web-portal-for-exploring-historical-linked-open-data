from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import login,logout,authenticate

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect('data_display:index')
    else:
        form = UserCreationForm()

    return render(request,'account/signup.html',{'form':form})
		
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            username = request.user.username
            loggedIn = True
            context = {'username':username,'loggedIn':loggedIn}
            return redirect('data_display:index')
    else:
        form = AuthenticationForm()
	
    return render(request,'account/login.html',{'formLogin':form})
		
def logout_view(request):
    logout(request)	
    return redirect('data_display:index')
		
def index(request):
    return redirect('data_display:index')