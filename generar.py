#!/usr/bin/python3

import glob

n_entradas_por_pagina = 10

def numeroTotalPaginas(n_entradas):
    n = int(n_entradas/n_entradas_por_pagina)
    if n_entradas%n_entradas_por_pagina > 0:
        n += 1
    return n

def getContenido(texto):
    linea_inicial = True
    titulo = ''
    html = ''
    for linea in texto.split('\n'):
        if linea_inicial:
            titulo = linea
            linea_inicial = False
        else:
            html += linea
    return [titulo, html]

def crearPagina(plantilla, texto, anterior, siguiente, path_salida):
    [titulo, html] = getContenido(texto)
    articulo = '<article>\n<h1>{0}</h1>\n{1}</article>'.format(titulo, html)
    navegacion = "<a href='{anterior}'>Anterior</a> <a href='{siguiente}'>Siguiente</a>".format(anterior=anterior, siguiente=siguiente)
    salida = plantilla.format(articulos=articulo, navegacion=navegacion)
    fout = open(path_salida, 'w')
    fout.write(salida)
    fout.close()

def crearIndices(plantilla, articulos, pagina, index_ok):
    html_articulos = ''
    for texto in articulos:
        [titulo, html] = getContenido(texto[1])
        articulo = '<article>\n<h1><a href="{2}">{0}</a></h1>\n{1}</article>\n'.format(titulo, html, texto[0])
        html_articulos += articulo
    anterior = 'index.html'
    if pagina-1 >= 0:
        anterior = 'index_{0}.html'.format(pagina-1)
    siguiente = 'index.html'
    if pagina+1 < len(lista_articulos)/n_entradas_por_pagina:
        siguiente = 'idex_{0}.html'.format(pagina+1)
    navegacion = "<a href='{anterior}'>Anterior</a> Página {actual} <a href='{siguiente}'>Siguiente</a>".format(anterior=anterior, siguiente=siguiente, actual=pagina+1)
    salida = plantilla.format(articulos=html_articulos, navegacion=navegacion)
    fout = open('index_{0}.html'.format(pagina), 'w')
    fout.write(salida)
    fout.close()
    if index_ok:
        fout = open('index.html'.format(pagina), 'w')
        fout.write(salida)
        fout.close()

fin = open('plantillas/plantilla.html', 'r')
plantilla = fin.read()
fin.close()

lista_articulos = glob.glob('articulos/*.html')
lista_articulos.sort()

pagina = numeroTotalPaginas(len(lista_articulos))-1
articulos=[]
index_ok = True
i = len(lista_articulos)-1
while i>-1:
    print('Procesando: {0}'.format(lista_articulos[i]))
    fin = open(lista_articulos[i], 'r')
    texto = fin.read()
    fin.close()
    articulos.append(['pagina_{0}.html'.format(i), texto])
    anterior = 'index.html'
    if i-1 >= 0:
        anterior = 'pagina_{0}.html'.format(i-1)
    siguiente = 'index.html'
    if i+1 < len(lista_articulos):
        siguiente = 'pagina_{0}.html'.format(i+1)
    crearPagina(plantilla, texto, anterior, siguiente, 'pagina_{0}.html'.format(i))
    if len(articulos) == n_entradas_por_pagina:
        crearIndices(plantilla, articulos, pagina, index_ok)
        articulos=[]
        pagina -= 1
        index_ok = False
    i -= 1

if len(articulos)>0:
    crearIndices(plantilla, articulos, pagina, index_ok)