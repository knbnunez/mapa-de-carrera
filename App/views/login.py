from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

from django.conf import settings

def login_view(request):
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            allowed_domains = settings.ALLOWED_EMAIL_DOMAINS
            if not any(username.endswith(domain) for domain in allowed_domains):
                messages.error(request, 'Dominio de correo no permitido')
                return redirect('login')
            return redirect('docente')
           # login(request, user)
         #   return redirect('docente')
        
        else:
            messages.error(request, 'Credenciales invalidas')
            # Manejar el caso de credenciales inválidas
            # pass
    return render(request, 'login.html')

#def logout_view(request):
 #   logout(request)
 #   return redirect('login')
