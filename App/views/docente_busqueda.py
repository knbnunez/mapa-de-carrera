# app/views.py
html lang="en">
 
<head>

    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.4.1/dist/css/bootstrap.min.css" integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.8.1/font/bootstrap-icons.css">
   
    
    <title>MDC</title>
</head>

<body>

<!--
    <div class="container">
        <div class="row">
            <div class="col-md-12 search">
                <form method="get">
                    <div id="custom-search-input">
                        <div class="input-group col-md-as">
                            <input type="text" class="form-control" placeholder="Buscar" name="Buscar"></input>
                            <span class="input-group-list">
                                <i class="icon icon-search"></i>
                                <button type="submit" class="boton btn-success">Buscar</button>
                            </span>
                        </div>
                     </div>
                </form>
            </div>
        </div>
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
