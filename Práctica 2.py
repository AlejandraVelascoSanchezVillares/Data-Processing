#PRACTICA 2: ECUALIZACIÓN DE IMÁGENES - INFORMÁTICA  30/01/2015 Facultad de Ciencias Matemáticas. Curso 2014-2015. 

#En primer lugar, invocamos el modulo PIL (Python Imaging Library) y abrimos la imagen que queremos modificar.
from PIL import Image
i=Image.open("tesla_bw.png",'r')
i.show()

#Funcion de histograma: calculamos el número de veces que se da cada valor de cada pixel de la imagen que queremos modificar y almacenamos estos datos en la lista f.
def histograma(i):
    f=[0]*256
    x=i.size[0]
    y=i.size[1]
    for j in range(x):
        for k in range(y):
            aux=i.getpixel((j,k))
            f[aux]=f[aux]+1
    return f

f=(histograma(i))

#Funcion de distribución acumulativa: creamos una lista cuyos elementos contengan la frecuencia en que se dan mas la de todos sus elementos anteriores.
def distribucion_acumulativa(f):
    l=[0]*256
    aux=0
    for i in range(len(f)):
        aux=aux+f[i]
        l[i]=aux
    return l

l=(distribucion_acumulativa(f))

#Funcion de dibujo: otorga visualizar mejor los resultados obtenidos hasta ahora.
def dibujo_histograma_distribucion_acumulativa(f,l):
    k=2
    ancho=256*k
    alto=128*k
    bg_color=110
    f_color=210
    l_color=0
    resultado=Image.new('L',(ancho,alto),bg_color)
    aspecto_factor_f=float(alto-1)/max(f)
    aspecto_factor_l=float(alto-1)/l[255]
    for x in xrange(256):
        for y in xrange(alto-1-int(f[x]*aspecto_factor_f),alto-1):
            resultado.putpixel((k*x,y),f_color)
        resultado.putpixel((k*x,alto-1-int(l[x]*aspecto_factor_l)),l_color)
    return resultado

resultado=(dibujo_histograma_distribucion_acumulativa(f,l))

resultado.show()

#Funcion tabla: se activa cada vez que la funcion siguiente necesita de ella.
def tabla(v):
    n=0
    while(l[n]==0):
        n+=1
    minimo=float(l[n])
    return int(round((l[v]-minimo)/(l[255]-minimo)*255))

#Funcion transformacion: los datos de la funcion anterior se recogen en la tabla.
def transformacion(l):
    t=[]
    for c in range(256):
        t.append(tabla(c))
    return t

#Funcion ecualizacion: recorre la imagen que creamos asignandole a cada elemento el pixel modificado.
def ecualizacion(i):
    t=(transformacion(l))
    ancho,alto=i.size
    bg_color=110
    ni=Image.new('L',(ancho,alto),bg_color)
    for j in xrange(ancho):
        for k in xrange(alto):
            ni.putpixel((j,k),t[i.getpixel((j,k))])
    return ni

pic=ecualizacion(i)
pic.show()
f_t=histograma(pic)
l_t=distribucion_acumulativa(f_t)
resultado_t=dibujo_histograma_distribucion_acumulativa(f_t,l_t)
resultado_t.show()
