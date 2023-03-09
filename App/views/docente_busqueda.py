# app/views.py
class DocenteBusquedaView(TemplateView):
    template_name = 'buscadocente.html'
    username='mapumapa'
    password='Mowozelu28'
    url_mapuche = 'http://10.7.180.231/mapuche/rest/'

    def get(self, request):
        url = reverse('buscadocente')
        url_buscadocente = self.url_mapuche+'agentes' # /agentes/{legajo}
        response = requests.get(url_buscadocente, auth=(self.username, self.password))
        # if response.status_code == 200:
        docentes = response.json()
        # print(docentes)
        
        return render(request, self.template_name, {'docentes': docentes})
        # else :
            # return render(request, self.template_name, {"docentes":})
    def busca(request):
       # url=self.url_mapuche+'agentes/'+legajo
        queryset = request.Get.get('q')
        if queryset:
            docentes = Docente.objects.filter(legajo=queryset).first()
            if docentes:
                url = reverse('docentes', kwargs={'legajo':queryset})
              #  return redirect('docentes', legajo=queryset)
     #    if queryset:
      #         docentes = Post.objects.filter(
      #             Q(legajo = queryset) 
      #         )
      #   responses = [requests.get(url, auth=(self.username, self.password), timeout=5) for url in [url]]
      #  return render(request, 'docente-detalle.html', {'docentes': json.dumps(docentes),'queryset':queryset} )
        return render(request, 'buscadocente.html', {'queryset':queryset} )
    </div>

    <form action="http://127.0.0.1:8000/docente" method="get">
        <label for="search_query">Buscar:</label>
        <input type="text" name=" " id="search_query">
        <button type="submit">Buscar</button>
      </form>

      <form id="mi-formulario" method="post">
        <label for="search_query">Buscar:</label>
        <input type="text" name="q" id="search_query">
        <input type="hidden" name="legajo" >
        
        <button type="submit">Buscar</button>
      </form>
      
      <script>
        const formulario = document.querySelector('#mi-formulario');
           formulario.addEventListener('submit', (event) => {
          event.preventDefault();
          const q = encodeURIComponent(document.querySelector('#search_query').value);
          const legajo = encodeURIComponent(document.querySelector('input[name="legajo"]').value);
          const url = `http://127.0.0.1:8000/docente/${legajo}`;
          window.location.href = url;
        });
      </script>-->
    <h1>Ingrese Legajo a buscar</h1>
    <form action="{% url 'buscadocente' %}" method="busca">
        <input type="text" name="q" value="{{ queryset }}">
        <button type="submit">Buscar</button>
    </form>
    

    {% for d in docentes %}
        <h3> - Nro DNI: {{d.numero_documento}}</h3>
        <h3> - Legajo: {{d.legajo}}</h3>
        <h3> - Nombre y Apellido: {{d.nombre_apellido}}</h3>
    {% endfor %}
</body>

</html>
