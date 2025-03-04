import numpy as np
import random
import ruleta
global TAM_POBLACION
TAM_POBLACION = 100

class Poblacion:
    def __init__(self):
        self.poblacion = []

    def evaluaPoblacion(self):
        for individuo in self.poblacion:
            individuo.evaluaAptitud()

    def seleccionaPadre(self):
        #return random.choice(self.poblacion)
        return ruleta(self.poblacion)
    

    def seleccionaSobrevivientes(self):
        self.poblacion.sort(key=lambda x: x.aptitud, reverse=True)
        self.poblacion = self.poblacion[:len(self.poblacion)/2]  # Se conservan los mejores 50 individuos

    def mejorIndividuo(self):
        return max(self.poblacion, key=lambda x: x.aptitud)

    def promedioAptitud(self):
        return sum(individuo.aptitud for individuo in self.poblacion) / len(self.poblacion)
    
class Individuo:
    def __init__(self):
        self.cromosoma = np.random.randint(0, 2, 10).tolist()
        self.aptitud = 0

    def evaluaAptitud(self):
        self.aptitud = sum(self.cromosoma)

    def __repr__(self):
        return f"Individuo({self.cromosoma}, Aptitud: {self.aptitud})"

def algoritmoGenetico(TAM_POBLACION, pCruza, pMuta, max_generaciones=100):
    poblacion = Poblacion()
    poblacion.poblacion = generaPoblacion(TAM_POBLACION)
    poblacion.evaluaPoblacion()

    generacion = 0  # Contador de generaciones

    while generacion < max_generaciones:
        padres = seleccionaPadres(poblacion.poblacion)
        hijos = []

        for i in range(0, len(padres), 2):
            if i+1 < len(padres) and random.random() <= pCruza:
                hijos.append(cruzaUnPunto((padres[i], padres[i+1])))

        for hijo in hijos:
            if random.random() <= pMuta:
                muta(hijo)

        for hijo in hijos:
            hijo.evaluaAptitud()

        poblacion.poblacion = seleccionaSobrevivientes(poblacion.poblacion, hijos)

        generacion += 1  # Incrementar el número de generaciones

        print(f"Generación {generacion}")
        print("Mejor individuo: ", poblacion.mejorIndividuo())
        print("Aptitud del mejor individuo: ", poblacion.mejorIndividuo().aptitud)
        print("Promedio de aptitud de la población: ", poblacion.promedioAptitud())

    print("Finalizó el algoritmo por límite de generaciones.")


def generaPoblacion(tam_pob):
    return [Individuo() for _ in range(tam_pob)]

def aptitud(individuo):
    return sum(gene * (i**2) for i, gene in enumerate(individuo.cromosoma))

def seleccionaPadres(poblacion):
    promedio = sum(aptitud(ind) for ind in poblacion) / len(poblacion)
    return [ind for ind in poblacion if aptitud(ind) > promedio]

def seleccionaSobrevivientes(padres, hijos):
    nueva_poblacion = padres + hijos
    nueva_poblacion.sort(key=lambda x: x.aptitud, reverse=True)
    return nueva_poblacion[:50]

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

# Ejecutar el algoritmo genético
algoritmoGenetico(100, 0.5, 0.2)
