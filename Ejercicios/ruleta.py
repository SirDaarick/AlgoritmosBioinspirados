import random

I1 = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1]
I2 = [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0]
I3 = [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1]
I4 = [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1]
I5 = [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]
I6 = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]


def aptitud(individuo):
    aux = 0
    for i in range(len(individuo)):
        aux += individuo[i]*(i**2)
    return aux

def ruleta(*poblacion):
    aptitudes = [aptitud(individuo) for individuo in poblacion]
    aptitud_total = sum(aptitudes)
    
    probabilidades = [aptitud / aptitud_total for aptitud in aptitudes]
    print("individuos", poblacion)
    print("aptitudes", aptitudes)
    print("probabilidades", probabilidades)
    
    aleatorio = random.random()
    print("Numero aleatorio entre 0 y 1", aleatorio)
    
    acumulado = 0
    
    for i, probabilidad in enumerate (probabilidades):
        acumulado += probabilidad
        if aleatorio <= acumulado:
            list(poblacion).remove(poblacion[i])
            print("Gano ", poblacion[i])
            
            return ruleta(poblacion)
            #return poblacion[i]
            
            
prueba1 = ruleta(I1, I2, I3, I4, I5, I6)
prueba2 = ruleta

print(prueba1, " fin prueba 1")
print(prueba2)
        
