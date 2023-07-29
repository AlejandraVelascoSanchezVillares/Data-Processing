

     # PRÁCTICA 1: NOTAS FINALES - INFORMÁTICA                               24 de Noviembre de 2014. Facultad de Ciencias Matemáticas. Curso 2014-2015.


#Presento aquí la función que define el cálculo de la nota final de la asignatura de Informática. En ella, se debe tener en cuenta el orden de introducción de las notas iniciales; puesto que:
     #e1: nota del primer examen o examen de Febrero
     #e2: nota del segundo examen o examen de Junio
     #p1: nota de la primera práctica
     #p2: nota de la segunda práctica
     #p3: nota de la tercera práctica
     #p4: nota de la cuarta práctica
     #p: nota de participación
     
#Considero también conveniente comentar que la función está diseñada para devolver un aviso de error al introducir datos erróneos (que no sean números del 0 al 10, 0 y 10 incluidos),
     #intervengan o no en la nota final. Además, en caso de no haberse hecho algún examen, el dígito que se debe introducir en la función en ese apartado es 0. Si esto no se lleva a cabo,
     #la función también avisará de ese error en los datos.


def nota(e1,e2,p1,p2,p3,p4,p):
    examenes=(0.125*e1+0.375*e2)
    practicas=(0.04*p1+0.08*p2+0.12*p3+0.16*p4)
    participacion=(0.1*p)
    if((2<=examenes)and(examenes<=5)and(1<=practicas)and(practicas<=4)and(0<=participacion)and(participacion<=1)):
        final=(examenes+practicas+participacion)
    elif((0<=practicas)and(practicas<1)and(0<=participacion)and(participacion<=1)and(0==examenes)):
        final=(practicas/40.0*100)
    elif((0<=examenes)and(examenes<2)and(1<=practicas)and(practicas<=4)and(0<=participacion)and(participacion<=1)):
        final=(examenes/50.0*100)
    else:
        final='error en los datos introducidos'
    return final

                                                                                         # Alejandra Velasco Sánchez-Villares. Grupo E. Subgrupo 3.
