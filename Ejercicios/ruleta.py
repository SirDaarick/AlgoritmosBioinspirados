import random
I1 = [1,0,0,1,1,1,0,0,1,0,1,1,0,0,1]
I2 = [1,1,1,1,1,1,1,1,0,0,0,0,0,0,0]
I3 = [0,0,0,0,0,0,0,0,1,1,1,1,1,1,1]
I4 = [1,0,1,0,1,0,1,0,1,0,1,0,1,0,1]
I5 = [0,1,0,1,0,1,0,1,0,1,0,1,0,1,0]
I6 = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]

poblacion = [I1, I2, I3, I4, I5, I6]

def aptitud(individuo):
    aux = 0
    for i in range(len(individuo)):
        aux += individuo[i]*(i**2)
    return aux

def ruleta(poblacion):
    aptitudes = [aptitud(individuo) for individuo in poblacion]
    aptitud_total = sum(aptitudes)
    
    probabilidades = [aptitud / aptitud_total for aptitud in aptitudes]
    print("\nIndividuos: ", *poblacion, sep="\n\t")
    print("\nAptitudes: ", aptitudes)
    print("\nProbabilidades:", *probabilidades, sep="\n\t")
    
    aleatorio = random.random()
    print("\nNumero aleatorio entre 0 y 1 = ", aleatorio)
    
    acumulado = 0
    
    for i, probabilidad in enumerate (probabilidades):
        acumulado += probabilidad
        if aleatorio <= acumulado:
            return poblacion[i]
            

    #se añaden los parametros "Tiradas" para controlar las veces que se ejecuta 
    #la ruleta y ganador con un valor predeterminado de none en caso de que sea 
    #la primer tirada
def ruleta_remplazo(individuos, tiradas = 0, ganador = None ): 

    #Se verifica si el ganador aun esta en la lista para elminarlo, si no esta o no hay
    #un ganador aun, entonces se utiliza la poblacion original
    if ganador in individuos:
        poblacion = list(individuos)
        poblacion.remove(ganador)
    else:
        poblacion = individuos

    aptitudes = [aptitud(individuo) for individuo in poblacion]
    aptitud_total = sum(aptitudes)
    
    probabilidades = [aptitud / aptitud_total for aptitud in aptitudes]
    print("\nIndividuos: ", *poblacion, sep="\n\t")
    print("\nAptitudes: ", aptitudes)
    print("\nProbabilidades:", *probabilidades, sep="\n\t")
    
    aleatorio = random.random()
    print("\nNumero aleatorio entre 0 y 1 = ", aleatorio)
    
    acumulado = 0
    
    for i, probabilidad in enumerate (probabilidades):
        acumulado += probabilidad
        if aleatorio <= acumulado:

            #Si las tiradas son 0, entonces retorna el ganador, y si aun quedan tiradas
            #se resta una y se llama recursivamente a la funcion para obtener los 
            #ganadores deseados
            if tiradas != 0:
                tiradas -= 1
                return ruleta_remplazo(poblacion,tiradas, poblacion[i])
            else:
                return poblacion[i]
            


def cruce_uniforme(padre1, padre2):
    hijo1 = []
    hijo2 = []
    for i in range(len(padre1)):
        if random.random() < 0.5: 
            hijo1.append(padre1[i])
            hijo2.append(padre2[i])
        else:
            hijo1.append(padre2[i])
            hijo2.append(padre1[i])
    return [hijo1, hijo2]

def cruce_punto(padre1, padre2):
    hijo1 = []
    hijo2 = []
    punto_cruce = random.randint(1, len(padre1) - 2) 

    for i in range(len(padre1)):
        if i < punto_cruce: 
            hijo1.append(padre1[i])
            hijo2.append(padre2[i])
        else:
            hijo1.append(padre2[i])
            hijo2.append(padre1[i])
    return [hijo1, hijo2]

def mutacion(individuo, porcMuta):
    individuo_mutado = []
    for i in range(len(individuo)):
        if random.random() < porcMuta: 
            if individuo[i] == 1:
                individuo_mutado[i] = 0
            else:
                individuo_mutado[i] = 1 
    return individuo_mutado

porcMuta = [0.01, 0.1, 0.2, 0.5]

def mutacion(individuo, porcMuta):
    individuo_mutado = individuo
    for i in range(len(individuo)):
        if random.random() < porcMuta: 
            if individuo[i] == 1:
                individuo_mutado[i] = 0
            else:
                individuo_mutado[i] = 1 
    return individuo_mutado

muta = mutacion(I6, porcMuta[3])
print(*muta)

#hijos = cruce_punto(I2,I3)
#aptitud1 = aptitud(hijos[0])
#aptitud2 = aptitud(hijos[1])

#print(*hijos[0], aptitud1, "\n", *hijos[1], aptitud2)

