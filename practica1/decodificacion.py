import random
import math
cromosoma = [0,1,1,1,0,1,1,1,1,1,1,0,1,0,1,1,1,1,1,1,0,1,0,1,0]
n = 5
n_alelos = n**2
n_reglas = math.ceil(n/2)

#for i in range(0,n_alelos):
#    cromosoma.append(random.randint(0,1))

#print(cromosoma)
#print(len(cromosoma))

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

decodificar(cromosoma, n)

#print(a_columnas(cromosoma, n))
decodificar(a_columnas(cromosoma,n),n)