from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

# Para consumo de la API
from App.models.mapa_de_carreras import Docente
from requests.exceptions import ConnectTimeout
import requests

def cargar_base(request):
    print("Comenzando a cargar_base...")
    username='mapumapa'
    password='Mowozelu28'
    url_mapuche = 'http://10.7.180.231/mapuche/rest'
    try:
        url_buscadocente = url_mapuche+'/agentes'
        response = requests.get(url_buscadocente, auth=(username, password), timeout=5)
        if response.status_code == 200:
            docentes = response.json() # json() convierte a diccionario de python    
            # Recuperar escalafón 'docentes'
            aux = []
            for d in docentes:
                cargos = requests.get(url_buscadocente+f"/{d['legajo']}/cargos", auth=(username, password)).json()
                es_docente = False
                for c in cargos:
                    if('nodo' not in c['escalafon'].lower().replace(" ", "")): # Con esta normalización de texto, cualquier escalafon <> a 'nodo' (no docente) es considera docente
                        es_docente = True
                        break # Salgo del bucle
                if(es_docente): 
                    # print("cargando docente...")
                    ## UPDATE --
                    if Docente.objects.filter(legajo=d['legajo']).exists(): 
                        docente = Docente.objects.get(legajo=d['legajo'])
                        docente.numero_documento = d['numero_documento']
                        docente.nombre_apellido  = d['agente']
                        docente.save() # No actualizo el legajo porque no tiene sentido... Si se hubiese cambiado el legajo no lo hubiese encontrado...
                    ## CREATE --
                    else:
                        docente = Docente.objects.create(
                            numero_documento = d['numero_documento'],
                            legajo           = d['legajo'],
                            nombre_apellido  = d['agente']
                        )
                    # aux.append(d)
            # docentes = aux # Almacenamos todos los 'docentes' recuperados
        # else: # status_code <> 200 --> Error --> Busco los datos de la base
            # docentes = Docente.objects.all() # Puede devolver vacío
    except ConnectTimeout: pass # timeout 5' --> Error
    
    print("Finalización de carga de base...")
    return redirect('docente')


def login_view(request):
    if request.method == 'POST':
        print("Se ejecuta esto?")
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        print(f"user: {user}")
        if user is not None:
            print("Autenticación FROM exitosa")
            login(request, user)
            cargar_base(request) # Además él mismo redirige a /docentes
            #return redirect('docente')
        else:
            # Manejar el caso de credenciales inválidas
            print("Autenticación FORM incorrecta")
            return redirect('login')
    #
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')