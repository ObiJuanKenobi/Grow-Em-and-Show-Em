from django.shortcuts import render, redirect
from django.contrib.auth import authenticate

def login_view(request):
     return render(request, 'login.html', {})
#    username = request.POST['username']
#    password = request.POST['password']
#    user = authenticate(username=username, password=password)
#    if user is not None:
#        return redirect('home')
#    else:
#        return render(request, 'login.html', {})
