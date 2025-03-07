import numpy as np
import random
import ruleta
global TAM_POBLACION
global N_ALELOS
TAM_POBLACION = 10  
N_ALELOS = 5


class Poblacion:
    def __init__(self):
        self.poblacion = []

    def evaluaPoblacion(self):
        for individuo in self.poblacion:
            individuo.evaluaAptitud()
    #NOTA: Verificar que la ruleta funcione para minimizar, ya que es lo que ocupa el nonograma 
    def seleccionaPadre(self):
        return ruleta(self.poblacion)
    
    
    #NOTA: Al seleccionar a los sobrevivientes, hay que tener en cuenta que siempre se debe de respetar los limites de la poblacion 
    def seleccionaSobrevivientes(self):
        self.poblacion.sort(key=lambda x: x.aptitud, reverse=True)
        self.poblacion = self.poblacion[:len(self.poblacion)/2]  # Se conservan los mejores 50 individuos

    def mejorIndividuo(self):
        return max(self.poblacion, key=lambda x: x.aptitud)
    
    def peorIndividuo(self):
        return min(self.poblacion, key=lambda x: x.aptitud)

    def promedioAptitud(self):
        return sum(individuo.aptitud for individuo in self.poblacion) / len(self.poblacion)
    
class Individuo:
    def __init__(self):
        self.cromosoma = np.random.randint(0, 2, N_ALELOS).tolist()
        self.aptitud = 0

    def evaluaAptitud(self):
        self.aptitud = aptitud(self)
        #self.aptitud = sum(self.cromosoma)

    def __repr__(self):
        return f"Individuo({self.cromosoma}, Aptitud: {self.aptitud})"
    

##NOTA: Agregar una forma de almacenar el mejor, peor y el promedio de los individuos segun la aptitud, y agregar una funcion para 
#graficar estos datos

##Agregar el criterio de paro para cuando se cumple el valor maximo o minimo de la funcion objetivo, en el caso del 
#nonograma, es minimizar, es decir 0 y hacer algo para no tener en cuenta el numero maximo de generaciones, ademas el la funcion 
#debe de recibir la semilla del random 

##Cambiar el criterio de paro con Epsilon en lugar de simplemente igualar las funciones
def algoritmoGenetico(TAM_POBLACION, pCruza, pMuta, max_generaciones=100):
    poblacion = Poblacion()
    poblacion.poblacion = generaPoblacion(TAM_POBLACION)
    poblacion.evaluaPoblacion()
    print("\nPoblacion", *poblacion.poblacion, "\n")
    generacion = 0  # Contador de generaciones

    while (generacion < max_generaciones): #Criterio de paro 1
        padres = seleccionaPadres(poblacion.poblacion)
        print("\nPadres", padres)
        hijos = []

        for i in range(0, len(padres), 2):
            if i+1 < len(padres) and random.random() <= pCruza:
                hijos.append(cruzaUnPunto((padres[i], padres[i+1])))

        for hijo in hijos:
            if random.random() <= pMuta:
                muta(hijo)

        for hijo in hijos:
            hijo.evaluaAptitud()
        print("\nHijos", hijos)
        poblacion.poblacion = seleccionaSobrevivientes(poblacion.poblacion, hijos)
        print("\nPobracion sobreviviente", poblacion.poblacion)
        generacion += 1  # Incrementar el número de generaciones

        print(f"Generación {generacion}")
        print("Mejor individuo: ", poblacion.mejorIndividuo())
        print("Aptitud del mejor individuo: ", poblacion.mejorIndividuo().aptitud)
        print("Promedio de aptitud de la población: ", poblacion.promedioAptitud(), "\n")
        if poblacion.mejorIndividuo() == poblacion.peorIndividuo(): #Criterio de paro 2
            break

    print("Finalizó el algoritmo por límite de generaciones.")


def generaPoblacion(tam_pob):
    return [Individuo() for _ in range(tam_pob)]

#Nonograma
#NOTA: se debe de poder decodificar en reglas para verificarlas que funcionan
def nonograma(individuo, reglas_r, reglas_c):
    nr = len(reglas_r)
    qr = len(reglas_r[0])
    nc = len(reglas_c)
    qc = len(reglas_c[0])
    
    if len(individuo) != nr * nc:
        raise ValueError(f"la longitud de la cadena debe ser de {nr*nc}")
    
    matriz = []
    
    for i in range(0, 25, 5):
        renglon = individuo[i:i+5]
        matriz.append(renglon)
        
    for regla in reglas_r:
        for condicion in reversed(regla):
            if condicion == 0:
                break
            
    
    
    

def obtener_columna(matriz, columna):
    columna = [fila[columna] for fila in matriz]
    return columna

#Funcion objetivo sencilla
#def aptitud(individuo):
 #   return sum(gene * (i**2) for i, gene in enumerate(individuo.cromosoma))

def aptitud(individuo):
    aux = 0
    for i in range(len(individuo.cromosoma)):
        aux += individuo.cromosoma[i]*(i**2)
    return aux

def seleccionaPadres(poblacion):
    promedio = sum(aptitud(ind) for ind in poblacion) / len(poblacion)
    return [ind for ind in poblacion if aptitud(ind) > promedio]

def seleccionaSobrevivientes(padres, hijos):
    nueva_poblacion = padres + hijos
    nueva_poblacion.sort(key=lambda x: x.aptitud, reverse=True)
    return nueva_poblacion[:50]

#NOTA: Agregar un punto de cruza de n puntos, donde n sea un porcentaje de la longitud del cromosoma
def cruzaUnPunto(pareja):
    pCruza = random.randint(1, len(pareja[0].cromosoma) - 1)
    hijo1 = Individuo()
    hijo2 = Individuo()

    hijo1.cromosoma[:pCruza] = pareja[0].cromosoma[:pCruza]
    hijo1.cromosoma[pCruza:] = pareja[1].cromosoma[pCruza:]

    hijo2.cromosoma[:pCruza] = pareja[1].cromosoma[:pCruza]
    hijo2.cromosoma[pCruza:] = pareja[0].cromosoma[pCruza:]

    return hijo1 if random.random() < 0.5 else hijo2  # Se elige uno de los dos hijos

def muta(hijo):
    pos = random.randint(0, len(hijo.cromosoma) - 1)
    hijo.cromosoma[pos] = 1 - hijo.cromosoma[pos]  # Mutación binaria (0↔1)

reglas_r = [(0,0,3), (0,0,5), (1,1,1), (0,0,5), (0,1,1)]
reglas_c = [(0,0,3), (0,2,2), (0,0,4), (0,2,2), (0,0,3)]
# Ejecutar el algoritmo genético
algoritmoGenetico(10, 0.5, 0.2, 10)


#NOTA: hacer una funcion que sea capaz de evaluar el 