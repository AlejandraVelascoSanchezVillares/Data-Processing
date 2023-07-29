from math import sqrt,acos
#from sypmy import *

#La función is_number_type sirve para comprobar si los datos introducidos son del tipo requerido para las clases que hemos creado.
def is_number_type(n):
    return isinstance(n,int)or isinstance(n,float) or isinstance(n,Expr)

class Vector(object):
    #Las funciones "__init__" determinan los elementos de la clase en la que se encuentran; y es en ellas donde se implementa la función is_number_type.
    def __init__(self,vx,vy):
        if is_number_type(vx) and is_number_type(vy):
            self.x=vx
            self.y=vy
        else:
            raise Exception('Datos erróneos para la construcción del Vector')
    #Las funciones "__repr__" son las solicitadas por el enunciado para mostrar por pantalla las coordenadas de los elementos de las clases dadas.
    def __repr__(self):
        return 'Vector('+str(self.x)+','+str(self.y)+')'
    #La funcion "dot" calcula el producto escalar entre dos vectores.
    def dot(self,other):
        return self.x*other.x+self.y*other.y
    #La función "__add__" calcula la suma de dos vectores.
    def __add__(self,other):
        return Vector(self.x+other.x,self.y+other.y)
    #La función "norm" calcula la norma de un vector(la raíz cuadrada del producto escalar de un vector por él mismo).
    def norm(self):
        return sqrt(self.dot(self))
    #La función "unit" calcula el vector unidad del vector dado, dividiéndolo por su norma.
    def unit(self):
        return Vector(self.x/self.norm,self.y/self.norm)
    #La función "ortogonal" devuelve un vector ortogonal(es decir, perpendicular) al dado, a partir de intercambiar sus coordenadas y cambiar uno de los signos de estas.
    def ortogonal(self):
        return Vector(-self.y,self.x)
    #La función "is_parallel" determina si los vectores dados son paralelos entre sí, o lo que es lo mismo, si el producto escalar de un vector y el ortogonal del otro es 0.
    def is_parallel(self,other):
        return self.dot(other.ortogonal())==0
    #La función "rotate" devuelve el vector resultado de girar el introducido en la función el ángulo o angle alrededor del punto (0,0).
    def rotate(self,angle):
        return Vector(self.x*cos(angle)-self.y*sin(angle),self.x*sin(angle)+self.y*cos(angle))

class Point(object):
    def __init__(self,px,py):
        if is_number_type(px) and is_number_type(py):
            self.x=px
            self.y=py
        else:
            raise Exception('Datos erróneos para la construcción del Punto')
    def __repr__(self):
        return'Point('+str(self.x)+','+str(self.y)+')'
    #La función "__add__" traslada el punto mediante un vector.
    def __add__(self,v):
        return Punto(self.x+v.x,self.y+v.y)
    #La función "vector_to" determina el vector de la linea que pasa por dos puntos.
    def vector_to(self,other): 
        Vector(other.x-self.x,other.y-self.y)
    #La función "line_to" devuelve la linea que pasa por dos puntos.
    def line_to(self,other):
        return Line(self,self.vector_to(other))
    #La siguiente función "distance" devuelve la distancia comprendida entre dos puntos calculando el vector unitario comprendido entre ellos. En general, y para todas las funciones "distance"
    # que vayamos encontrando a partir de ahora, en caso de no tratarse de dos figuras de la clase en la que se encuentra la función "distance" que está siendo ejecutada o de una clase menos
    # compleja, la función ejecutaría otra función "distance" diferente, perteneciente a la clase del elemento introducido más complejo.
    def distance(self,other):
        if isinstance(other,Point): #distancia punto a punto
            return self.vector_to(other).norm()
        else:
            return other.distance(self)
    #Las funciones "intersects" establecen, a partir de determinar si la distancia entre ambas figuras es cero, caso en el que intersecarían, si existe intersección entre las figuras o no. Al
    # igual que en las funciones "distance", si no se trata de dos figuras de la clase de la función que se está ejecutando o son menos complejas, se ejecutaría una función "intersects" diferente.
    def intersects(self,other):
        if isinstance (other,Point):
            return distance(self,other)==0
        else:
            return other.intersects(self)
        
class Line(object):
    #Tenemos que el elemento de la linea "normal" es el vector ortogonal unitario del vector que define la linea o recta.
    def __init__(self,point,vect):
        self.p=point
        self.v=vect
        self.normal=self.v.ortogonal().unit()
    def __repr__(self,p1,p):
        return'Line('+str(self.p)+','+str(self.v)+')'
    #La siguiente función "distance" devuelve la distancia comprendida entre un punto y una linea a partir del cálculo del producto escalar del vector ortogonal unitario de la recta y la
    # distancia entre el punto con el que contruimos la linea y el dado. Esta función también devuelve la distancia entre dos lineas dividiendo el caso en rectas paralelas y secantes. En el primer
    # caso, calculamos la distancia entre una recta y un punto de la otra(procedimiento ya definido en la clase Point) y en el segundo caso, la distancia es cero por ser secantes. 
    def distance(self,other):
        if isinstance(other,Point):
            v_orto=self.v.ortogonal().unit()
            return abs(v_orto.dot(self.p.vector_to(other)))
        elif isinstance(other,Line):
            if self.v.is_parallel(other.v):
                return self.distance(other.p)
            else:
                return 0
        else:
            return other.distance(self)
    def intersects(self,other):
        if isinstance (other,Point) or isinstance(other,Line):
            return distance(self,other)==0
        else:
            return other.intersects(self)

class Segment(object):
    #Tenemos que el elemento del segmento "v" es el vector entre los dos puntos que configuran el segmento, el elemento "length" es la norma del vector obtenido, "unit" es el vector unitario de "v"
    # y l es la linea en la que el segmento está contenido. El principio y fin del segmento viene por los "end".
    def __init__(self,p1,p2):
        if isinstance(p1,Point) and isinstance(p2,Point):
            self.end1=p1
            self.end2=p2
            self.v=p1.vector_to(p2)
            self.length=self.v.norm()
            self.unit=self.v.unit()
            self.l=Line(self.end1,self.v)
        else:
            raise Exception('Datos erróneos para la construcción del Segmento')
    def __repr__(self):
        return'Segment('+str(self.p1)+','+str(self.p2)+')'
    def distance(self,other):
        #La función para calcular la distancia entre un punto y un segmento se divide en tres casos dentro de otros dos consistentes en tratar los datos según la cercanía del punto dado a
        # cualquiera de los que conforman el segmento. Si el punto está más proximo a "end1", se ejecuta un caso, y si está más próximo a "end2", el otro. Dentro de estos dos casos, existen otros
        # tres para cada uno, que consisten en determinar si el ángulo que forman la linea que pasa por el punto y su "end" más cercano con el segmento es mayor o igual a 90º. Si es mayor o igual,
        # la distancia al segmento será la distancia del punto a su "end" más cercano y si es menor, la distancia del punto a la linea que pasa por el segmento.
        if isinstance(other,Point):
            end=min(self.end1.distance(other),self.end2.distance(other))
            if acos(self.end.vector_to(other).unit()*self.unit.ortogonal()/self.end.vector_to(other).unit().norm()*self.unit.ortogonal().norm())>=90:
                return self.end.distance(other)
            else:
                return other.distance(self.l)
        #La función para calcular la distancia entre una linea y un segmento se divide en tres casos: si la linea dada y la que contiene el segmento son paralelas(en cuyo caso la distancia se
        # obtendría a partir de la función ya definida de la distancia entre dos rectas), si la linea dada y la que contiene al segmento se cortan y además la distancia de los puntos extremos del
        # segmento a la recta son de igual signo(lo que indicaría que se encuentran ambos a la derecha o izquierda de la linea, lo que implicaría que el segmento no corta a la
        # recta, por lo que la distancia del segmento a esta sería la distancia más pequeña desde el "end" más próximo a la recta) y, por último, el caso en que el segmento corta a la recta: la
        # distancia es 0.
        elif isinstance(other,Line):
            if self.v.is_parallel(other.v):
                return self.distance(other.p)
            elif self.l.intersects(other)and ((self.end1.distance(other)<0 and self.end2.distance(other)<0) or (self.end1.distance(other)>0 and self.end2.distance(other)>0)):
                return min(self.end1.distance(other),self.end2.distance(other))
            else:
                return 0
        #La función para calcular la distancia entre dos segmentos se divide en dos casos: los segmentos se cortan(si los segmentos tienen distancias de igual signo a la linea que contiene al
        # otro segmento estos se cortan, y su distancia es 0) o los segmentos no se cortan(en este caso, la distancia consistiría en la menor de las formadas entre los extremos de los segmentos).
        elif isinstance(other,Segment):
            if self.l.intersects(other.l)and ((self.end1.distance(other.l)<0 and self.end2.distance(other.l)<0) or (self.end1.distance(other.l)>0 and self.end2.distance(other.l)>0))and((other.end1.distance(self.l)<0 and other.end2.distance(self.l)<0) or (other.end1.distance(self.l)>0 and other.end2.distance(self.l)>0)):
                return 0
            else:
                return min(self.end1.distance(other.end1),self.end1.distance(other.end2),self.end2.distance(other.end1),self.end2.distance(other.end2))
        else:
            other.distance(self)
    def intersects(self,other):
        if isinstance (other,Point)or isinstance(other,Line)or isinstance(other,Segment):
            return distance(self,other)==0
        else:
            return other.intersects(self)

class Circle(object):
    def __init__(self,center,radius):
        if isinstance(center,Point)and is_number_type(radius)and radius>0:
            self.center=center
            self.radius=radius
        else:
            raise Exception('Datos erróneos para la construcción del Círculo')
    def __repr__(self):
        return'Circle('+str(self.center)+','+str(self.radius)+')'
    #La siguiente función "distance" devuelve la distancia entre "other" y el centro del circulo.
    def distance(self,other):
        if isinstance(other,Point)or isinstance(other,Line)or isinstance(other,Segment):
            return center.distance(other)
        elif isinstance(other,Circle):
            return center.distance(other.center)
        else:
            return other.distance(self)
    #La siguiente función "intersects" determina si la distancia de "other" al centro es igual al radio del circulo; es decir, si "other" corta a la circunferencia del circulo.
    def intersects(self,other):
        if isinstance(other,Point)or isinstance(other,Line)or isinstance(other,Segment)or isinstance(other,Circle):
            return center.distance(other)==radium
        else:
            return other.distance(self)

class Triangle(object):
    #Tratamos como segmentos los lados del triángulo.
    def __init__(self,t1,t2,t3):
        if isinstance(t1,Point)and isinstance(t2,Point)and isinstance(t3,Point):
            self.t1=t1
            self.t2=t2
            self.t3=t3
            self.v12=Segment(t1,t2)
            self.v23=Segment(t2,t3)
            self.v31=Segment(t3,t1)
        else:
            raise Exception('Datos erróneos para la construcción del Triángulo')
    def __repr__(self):
        return'Triangle('+str(self.t1)+','+str(self.t2)+','+str(self.t3)+')'
    #La siguiente función "distance" determina la menor distancia entre los lados de los triángulos (segmentos) y la figura "other".
    def distance(self,other):
        if isinstance(other,Point)or isinstance(other,Line)or isinstance(other,Segment)or isinstance(other,Circle):
            return min(self.v12.distance(other),self.v23.distance(other),self.v31.distance(other))
        elif isinstance(other,Triangle):
            return min(self.v12.distance(other.v12),self.v23.distance(other.v23),self.v31.distance(other.v31),self.v12.distance(other.v23),self.v23.distance(other.v31),self.v31.distance(other.v12),self.v12.distance(other.v31),self.v23.distance(other.v12),self.v31.distance(other.v23))
        else:
            return other.distance(self)
    def instersects(self,other):
        if isinstance (other,Point)or isinstance(other,Line)or isinstance(other,Segment)or isinstance(other,Circle)or isinstance(other,Triangle):
            return self.distance(other)==0
        else:
            return other.intersects(self)

class Parallelogram(object):
    #Tratamos como segmentos los lados del paralelogramo.
    def __init__(self,vertex,v1,v2):
        if isinstance(vertex,Point)and isinstance(v1,Vector)and isinstance(v2,Vector):
            self.vertex=vertex
            self.v1=v1
            self.v2=v2
            self.op_vertex=vertex+(v1+v2)
            self.v1_vertex=v1+vertex
            self.v2_vertex=v2+vertex
            self.vertex_v1_vertex=Segment(vertex,v1_vertex)
            self.v1_vertex_op_vertex=Segment(v1_vertex,op_vertex)
            self.op_vertex_v2_vertex=Segment(op_vertex,v2_vertex)
            self.v2_vertex_v1_vertex=Segment(v2_vertex,v1_vertex)
        else:
            raise Exception('Datos erróneos para la construcción del Paralelogramo')
    def __repr__(self,p,v1,v2):
        return'Parallelogram('+str(self.vertex)+','+str(self.v1)+','+str(self.v2)+')'
    #La siguiente función "distance" determina la menor distancia de los lados del paralelogramo (segmentos) a la figura "other".
    def distance(self,other):
        if isinstance(other,Point)or isinstance(other,Line)or isinstance(other,Segment)or isinstance(other,Circle)or isinstance(other,Triangle):
            return min(self.v2_vertex_v1_vertex.distance(other),self.v1_vertex_op_vertex.distance(other),self.op_vertex_v2_vertex.distance(other),self.vertex_v1_vertex.distance(other))
        else:
            return min(self.v2_vertex_v1_vertex.distance(other.vertex_v1_vertex),self.v2_vertex_v1_vertex.distance(other.vertex_v1_vertex),self.v2_vertex_v1_vertex.distance(other.vertex_v1_vertex),self.v2_vertex_v1_vertex.distance(other.vertex_v1_vertex),self.v2_vertex_v1_vertex.distance(other.v2_vertex_v1_vertex),self.v1_vertex_op_vertex.distance(other.v2_vertex_v1_vertex),self.op_vertex_v2_vertex.distance(other.v2_vertex_v1_vertex),self.vertex_v1_vertex.distance(other.v2_vertex_v1_vertex),self.v2_vertex_v1_vertex.distance(other.v1_vertex_op_vertex),self.v2_vertex_v1_vertex.distance(other.v1_vertex_op_vertex),self.v2_vertex_v1_vertex.distance(other.v1_vertex_op_vertex),self.v2_vertex_v1_vertex.distance(other.v1_vertex_op_vertex),self.v2_vertex_v1_vertex.distance(other.op_vertex_v2_vertex),self.v2_vertex_v1_vertex.distance(other.op_vertex_v2_vertex),self.v2_vertex_v1_vertex.distance(other.op_vertex_v2_vertex),self.v2_vertex_v1_vertex.distance(other.op_vertex_v2_vertex))
    def instersects(self,other):
        return self.distance(other)==0
        
        
        
        
        
        
        
