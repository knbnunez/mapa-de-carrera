# with open("input.txt", "r", encoding="utf-8") as archivo_lectura: 
#     lista_cadenas = archivo_lectura.read().splitlines()

# for i in range(len(lista_cadenas)): 
#     lista_cadenas[i] = "('" + lista_cadenas[i].strip() + "'),\n"

# with open("output.txt", "w", encoding="utf-8") as archivo_escritura: 
#     archivo_escritura.writelines(lista_cadenas)

# TODO: Revisar cómo copiar muuuuchos registros de una sola columna,
#       si selecciono la columna sólo me trae los que puedo ver, o sea, los que cargó
#       hay que ver si se puede sacar la restricción...


# Generamos tantos archivos como columnas necesitemos.
with open("input1.txt", "r", encoding="utf-8") as input1, open("input2.txt", "r", encoding="utf-8") as input2, open("input3.txt", "r", encoding="utf-8") as input3, open("input4.txt", "r", encoding="utf-8") as input4:
    lista_cadenas1 = input1.read().splitlines()
    lista_cadenas2 = input2.read().splitlines()
    lista_cadenas3 = input3.read().splitlines()
    lista_cadenas4 = input4.read().splitlines()

lista_concatenada = []

for i in range(len(lista_cadenas1)):
    cadena_concatenada = "("+lista_cadenas1[i]+", '"+lista_cadenas2[i]+"', "+lista_cadenas3[i]+", "+lista_cadenas4[i]+")," # Y agregaríamos más comas entre strings
    lista_concatenada.append(cadena_concatenada)

with open("output.txt", "w", encoding="utf-8") as archivo_concatenado:
    archivo_concatenado.writelines(lista_concatenada)