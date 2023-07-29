import urllib
#import matplotlib.pyplot as plt
#import numpy as np

sanidad='http://transparencia.gob.es/es_ES/buscar/contenido/cibi/CIBI_DPTO26'
url=presidencia='http://transparencia.gob.es/es_ES/buscar/contenido/cibi/CIBI_DPTO25'
urls=[sanidad,presidencia]
nombres_ficheros=['sanidad','presidencia']

# EJERCICIO 1

def obtencion(cod_html,tag_inicio,tag_final):
    inicio=cod_html.find(tag_inicio)
    final=cod_html.find(tag_final)
    texto=cod_html[inicio+7:final]
    return texto

def retoque_columnas(c):
    tag1=c.find(';span class="tr-data--subtitle">')
    ret1=c[:tag1]+c[(c.find('>')+1):]
    tag2=ret1.find(';/span>')
    ret2=ret1[:tag2]+ret1[(ret1.find('>')+1):]
    tag3=ret2.find('class="tr-cell__measure tr-cell__num">')
    ret3=ret2[:tag3]+ret2[(ret2.find('>')+1):]
    tag4=ret3.find(';span class="tr-data__unit">m;sup>2;/sup>;/span>;')
    ret4=ret3[:tag4]+ret3[(ret3.find('>')+1):]
    tag5=ret4.find('m;sup>2;/sup>;/span>;')
    ret5=ret4[:tag5]+ret4[(ret4.find('>')+21):]
    ret=ret5+'m2'
    return ret

def obtencion_columnas(tag_inicio,tag_final,texto):
    columnas=''
    i=texto.find(tag_inicio)
    while i>=0 and i<=len(texto):
        inicio=texto.find(tag_inicio,i)
        final=texto.find(tag_final,i)
        c=texto[inicio+4:final+1]
        columna=c.replace('<',';')
        columnas=columnas+columna
        i=texto.find(tag_inicio,i+1)
    return columnas

def obtencion_fila(cuerpo,i):
    inicio=cuerpo.find('<tr>',i)
    final=cuerpo.find('</tr>',i)
    fila=cuerpo[inicio+4:final]
    return fila

def obtencion_filas(cuerpo):
    filas=''
    i=0
    while (i>=0 and i<=len(cuerpo)):
        fila=retoque_columnas(obtencion_columnas('<td','</td>',obtencion_fila(cuerpo,i)))
        filas=filas+'\n'+fila
        i=cuerpo.find('<tr>',i+1)
    return filas

def creacion_fichero(nombre_fichero,url):
    cod_html=urllib.urlopen(url).read()
    cabecera=obtencion(cod_html,'<thead>','</thead>')
    cuerpo=obtencion(cod_html,'<tbody>','</tbody>')
    th=obtencion_columnas('<th>','</th>',cabecera)[:-1]
    td=obtencion_filas(cuerpo)
    t=th+td
    fichero=open(nombre_fichero+'.txt','w')
    fichero.write(t)
    fichero.close()
    return fichero

def procesamiento_paginas(urls,nombres_ficheros):
    ficheros=[]
    for i in xrange(len(urls)):
        url=urls[i]
        nombre_fichero=nombres_ficheros[i]
        ficheros.append(creacion_fichero(nombre_fichero,url))
    return ficheros

# EJERCICIO 2

nombres_ficheros=['sanidad','presidencia']
cat='Uso'
pal='JUVENTUD'

def obtencion_categoria(fichero,cat):
    linea=fichero.readline()
    x=linea.split(';')
    return x.index(cat)
        
def busqueda(nombre_fichero,cat,pal):
    r=[]
    fichero=open(nombre_fichero+'.txt','r')
    categoria=obtencion_categoria(fichero,cat)
    lineas=fichero.readlines()
    for linea in lineas:
        if pal in linea:
            y=linea.split(';')
            for i in y:
                if pal in i:
                    z=y.index(i)
                    if categoria==z:
                        r.append(linea)
    return r

def filtro_paginas(nombres_ficheros,cat,pal):
    resultado=[]
    for i in range(len(nombres_ficheros)):
        resultado.append(busqueda(nombres_ficheros[i],cat,pal))
    return resultado

#EJERCICIO 3
    
def main(urls, file_names, cat, pal):
    processPages(urls, file_names)
    filtered = filterPages(file_names, cat, pal)
    plot(file_names, filtered, cat, pal)


def plot(file_names, filtered, cat, pal):
    numList = []
    for minist in filtered:
        numList.append(len(minist))
    y_pos = np.arange(len(numList))
    plt.barh(y_pos, numList, align='center', alpha=0.4)
    plt.yticks(y_pos, file_names)
    plt.xlabel('Cantidad')
    title = 'Ministerios con la cadena ' + pal + ' en la categoria ' + cat
    plt.title(title)
    
    plt.show()
