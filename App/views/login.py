from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('docente')
        else:
            # Manejar el caso de credenciales inválidas
            pass
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')
