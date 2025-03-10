import numpy as np
import random
import matplotlib.pyplot as plt
import math
global TAM_POBLACION
global N_ALELOS
TAM_POBLACION = 100  
N_ALELOS = 25

class Poblacion:
    def __init__(self):
        self.poblacion = []

    def evaluaPoblacion(self):
        for individuo in self.poblacion:
            individuo.evaluaAptitud()

    def seleccionaPadre(self):
        return ruleta_min(self.poblacion)
    

    def seleccionaSobrevivientes(self):
        self.poblacion.sort(key=lambda x: x.aptitud, reverse=False)
        self.poblacion = self.poblacion[:int(TAM_POBLACION)]  # Se conservan los mejores 50 individuos
    
    def mejorIndividuo(self):
        return min(self.poblacion, key=lambda x: x.aptitud)
    
    def peorIndividuo(self):
        return max(self.poblacion, key=lambda x: x.aptitud)

    def promedioAptitud(self):
        return sum(individuo.aptitud for individuo in self.poblacion) / len(self.poblacion)
    

class Individuo:
    def __init__(self):
        self.cromosoma = np.random.randint(0, 2, N_ALELOS).tolist()
        self.aptitud = 0

    def evaluaAptitud(self):
        self.aptitud = aptitud(self)

    def __repr__(self):
        return f"Individuo({self.cromosoma}, Aptitud: {self.aptitud})"
    

#Falta recibir semilla random

##Cambiar el criterio de paro con Epsilon en lugar de simplemente igualar las funciones
def algoritmoGenetico(TAM_POBLACION, pCruza, pMuta, max_generaciones=1000):
    poblacion = Poblacion()
    poblacion.poblacion = generaPoblacion(TAM_POBLACION)
    poblacion.evaluaPoblacion()
    print("\nPoblacion", *poblacion.poblacion, "\n")
    generacion = 0  # Contador de generaciones
    mejor, peor, promedio = [], [], []

    while (generacion < max_generaciones): #Criterio de paro 1
        padres = [poblacion.seleccionaPadre(), poblacion.seleccionaPadre()]
        hijos = []

        for i in range(0, len(padres), 2):
            if i+1 < len(padres) and random.random() <= pCruza:
                hijos.extend(cruzaNpuntos([padres[i], padres[i+1]], 0.5))

        for hijo in hijos:
            if random.random() <= pMuta:
                muta(hijo)

        for hijo in hijos:
            hijo.evaluaAptitud()
        
        poblacion.poblacion.extend(hijos)
        poblacion.seleccionaSobrevivientes()

        mejor.append(poblacion.mejorIndividuo().aptitud)
        peor.append(poblacion.peorIndividuo().aptitud)
        promedio.append(poblacion.promedioAptitud())

        
        generacion += 1  # Incrementar el número de generaciones

        print(f"Generación {generacion}")
        print("Mejor individuo: ", poblacion.mejorIndividuo())
        print("Aptitud del mejor individuo: ", poblacion.mejorIndividuo().aptitud)
        print("Promedio de aptitud de la población: ", poblacion.promedioAptitud(), "\n")

        if poblacion.mejorIndividuo().aptitud == 0:
            break

        if poblacion.mejorIndividuo() == poblacion.peorIndividuo(): #Criterio de paro 2
            break
    
    graficar(mejor, peor, promedio)
    print("Finalizó el algoritmo por límite de generaciones.")

def graficar(mejores, peores, promedios):
    generaciones = list(range(1, len(mejores) + 1))

    plt.figure(figsize=(8, 5))  
    plt.plot(generaciones, mejores, label="Mejor",  linestyle="-", color="blue")
    plt.plot(generaciones, peores, label="Peor", linestyle="-", color="red")
    plt.plot(generaciones, promedios, label="Promedio", linestyle="-", color="green")

    plt.xlabel("Generaciones")
    plt.ylabel("Valor de aptitud")
    plt.title("Evolución de la aptitud a lo largo de las generaciones")
    plt.legend()  
    plt.grid(True)  

    plt.show()

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


def aptitud(individuo):
    aux = 0
    for i in range(len(individuo.cromosoma)):
        aux += individuo.cromosoma[i]*(i**2)
    return aux

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

def ruleta_min(poblacion):
    aptitudes = [aptitud(individuo) for individuo in poblacion]
    
    max_apt = max(aptitudes) 
    aptitudes_invertidas = [max_apt - apt + 1 for apt in aptitudes]  
    
    aptitud_total = sum(aptitudes_invertidas)
    
    # Calcular probabilidades basadas en aptitudes invertidas
    probabilidades = [apt / aptitud_total for apt in aptitudes_invertidas]
    
    print("\nIndividuos: ", *poblacion, sep="\n\t")
    print("\nAptitudes originales (minimizar): ", aptitudes)
    print("\nAptitudes invertidas: ", aptitudes_invertidas)
    print("\nProbabilidades:", *probabilidades, sep="\n\t")
    
    aleatorio = random.random()
    print("\nNúmero aleatorio entre 0 y 1 = ", aleatorio)
    
    acumulado = 0
    for i, probabilidad in enumerate(probabilidades):
        acumulado += probabilidad
        if aleatorio <= acumulado:
            return poblacion[i]


def calcularFraccion(n, longitud_cromosoma):
    if not (0 < n <= 1):
        raise ValueError("La fracción debe estar entre 0 y 1.")
    puntos_cruza = max(1, int(n * longitud_cromosoma))
    return min(puntos_cruza, longitud_cromosoma - 1)

def cruzaNpuntos(pareja, fraccion):
    longitud_cromosoma = len(pareja[0].cromosoma)
    n = min(calcularFraccion(fraccion, longitud_cromosoma), longitud_cromosoma - 2)
    print(n)
    puntos = sorted(random.sample(range(1, longitud_cromosoma-1), n))
    
    hijo1 = []
    hijo2 = []
    
    padre1 = pareja[0].cromosoma
    padre2 = pareja[1].cromosoma
    inicio = 0
    intercambio = False
    
    for punto in puntos + [longitud_cromosoma]:
        if intercambio:
            hijo1.extend(padre2[inicio:punto])
            hijo2.extend(padre1[inicio:punto])
        else:
            hijo1.extend(padre1[inicio:punto])
            hijo2.extend(padre2[inicio:punto])
        inicio = punto
        intercambio = not intercambio

    nuevo_hijo1 = Individuo()
    nuevo_hijo2 = Individuo()
    nuevo_hijo1.cromosoma = hijo1
    nuevo_hijo2.cromosoma = hijo2
    return [nuevo_hijo1, nuevo_hijo2]

def a_columnas(cromosoma, n):
    columna = []
    for i in range(0, n):
        for j in range(0,n**2,n):
            columna.append(cromosoma[i+j])
    return columna

def decodificar(cromosoma, n):
    n_regla = math.ceil(n/2)
    reglas = []

    for j in range(0, n**2, n):
        regla = []
        n_unos = 0
        for i in range (0, n):
            if cromosoma[i+j]==1:
                n_unos += 1
            else:
                if n_unos == 0:
                    continue
                else:
                    regla.append(n_unos)
                    n_unos = 0
        if n_unos > 0:
            regla.append(n_unos)
        
        while len(regla) < n_regla:
            regla.append(0)
        
        reglas.append(regla)
    print(reglas)
    return reglas

reglas_r = [(0,0,3), (0,0,5), (1,1,1), (0,0,5), (0,1,1)]
reglas_c = [(0,0,3), (0,2,2), (0,0,4), (0,2,2), (0,0,3)]



algoritmoGenetico(10, 0.5, 0.2, 1000)
