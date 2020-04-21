import random
import math

'''
Laboratorio de Algoritmos genéticos:

Este archivo contiene las funciones que debe implementar para 
la práctica de laboratorio.

Ejercicio 1: operador de selección. Implementar la función selectRanking()
Ejercicio 2: operador de crossover. Implementar la función orderOneCrossover()
Ejercicio 3: operador de mutación. Implementar las funciones insertMutation() y swapMutation()

Instrucciones:
Este laboratorio cuenta con 2 archivos de código fuente de python:
    1. tsp.py: Programa principal que implementa la interfaz grafica y los parámetros para la ejecución
                del algoritmo genético a implementar. Leer este archivo para referencia del funcionamiento 
                general de la aplicación. En especial, revisar los métodos initHandler(), trainHandler() y nextHandler()
    2. genetic.py: Archivo con las funciones referentes a la implementación del algoritmo genético basado en permutaciones.
                En este archivo se implementa toda la funcionalidad referente al proceso de evolución de la población.

Para probar la aplicación o sus soluciones puede ejecutar el programa principal tsp.py usando: python tsp.py

'''

def initPopulation(cities, pop_size):
    '''
    Create a random list of candidate solutions.
    
    Return a list of candidates where each candidate is 
    a list of numbers corresponding to city ids.
    '''
    cities_id = [i for i in range(len(cities))]
    population = []
    for i in range(pop_size):
        candidate = cities_id.copy()
        random.shuffle(candidate)
        population.append(candidate)

    return population

def citiesDist(c1, c2, cities):
    '''
    Euclidian distance between 2 cities
    '''
    pos_c1 = cities[c1]['position']
    pos_c2 = cities[c2]['position']
    
    return math.sqrt((pos_c2[0] - pos_c1[0])**2 + (pos_c2[1] - pos_c1[1])**2)

def fitness(candidate, cities):
    '''
    returns the inverse of the travel cost for the given candidate
    '''
    total_dist = 0
    for i in range(len(candidate) - 1):
        total_dist += citiesDist(candidate[i], candidate[i + 1], cities)

    return 1/total_dist

def getBest(population, cities, fitness=fitness):
    best = max(population, key=lambda c: fitness(c, cities))
    return fitness(best, cities), best 

def getWorst(population, cities, fitness=fitness):
    worst = min(population, key=lambda c: fitness(c, cities))
    return fitness(worst, cities), worst

def selectRanking(population, cities):
    '''
    ----> Ejercicio 1 <----
    Implementar el operador de selección por el método del RANKING.
    
    Usted debe modificar esta función para realizar la operación 
    de selección de las soluciones más competentes por el método del ranking.

    Esta función recibe 2 valores:
      population: es una lista de listas con permutaciones del orden de las ciudades a visitar.
                    por ejemplo, para un problema con 3 ciudades y una poblacion de 2 soluciones:
                        population = [[0,2,1], [2,1,0]]
      cities: es una lista de datos para cada ciudad. cada elemento es un diccionario {'position':(x, y), 'id':<id del punto en el GUI>}
    
    Esta función debe retornar una lista con el mismo número de candidatos que la lista population

    Tips:
        - para calcular el fitnes de una solucion use lo siguiente: valor = fitness(candidato, cities), el candidato es un elemento
        de la lista population y cities es el mismo objeto que se recibe como parametro.
        - obtenga una nueva lista ordenada en forma descendente donde el primer elemento es el candidato más fuerte 
        o con valor de fitness mayor, y el último es el candidato más debil.
    '''
    # hace una copia de la poblacion
    pop = population.copy()
    # ordena en forma descendente
    # Se usa el argumento key invocando una funcion lambda
    # que llama a la funcion fitness, se debe usar la funcion lambda
    # ya que la funcion fitness requiere un argumento adicional 
    # que es la lista de ciudades, cities.
    pop.sort(reverse=True, key=lambda c: fitness(c, cities))
    
    # crea un ranking para los candidatos
    # estas operaciones asigna la cantidad de candidatos
    # mas fuertes para que se repliquen y los mas debiles 
    # se eliminen en la siguiente generacion
    rank = range(len(pop), 0, -1)
    valor_total = sum(rank)
    porcentajes = [r / valor_total for r in rank]
    proporcion = [p * len(pop) for p in porcentajes]
    final = [round(e) for e in proporcion]
    # Luego de tener el numero de candidatos
    new_generation = []
    # Generar los candidatos de acuerdo al numero 
    for i in range(len(pop)):
        for r in range(final[i]):
            new_generation.append(population[i])
    
    return new_generation

def orderOneCrossover(parent1, parent2):
    '''
    ----> Ejercicio 2 <----
    Implementar el operador de crossover de orden 1.

    Usted debe modificar esta función para realizar la operación de crossover de 2 candidatos padres.
    
    Esta función recibe 2 valores:
        parent1: candidato 1, una lista con una permutación de ids de ciudades, por ejemplo, 
                para un problema con 4 ciudades, un candidato podría ser: [3,1,0,2]
        parent2: otro candidato
            v     v
        [2, 4, 1, 0, 3] [0, 3, 2, 4, 1] => [ 2, 4, 1, 0, 3]

    Esta función debe retornar un nuevo candidato hijo producto del crossover de los padres.

    Procedimiento:
    Para implementar correctamente la operación de crossover de orden 1 se recomienda seguir los siguientes pasos:
        1. crear una lista vacia del mismo tamaño que cualquier padre.
        2. obtener los puntos de inicio y final aleatorios para el segmento a copiar del padre 1.
        3. insertar el segmento del padre 1 en la misma posición en el hijo.
        4. completar los elementos restantes, en orden, del padre 2.
        5. retornar la solución hijo.
    
    Tips:
        - use funciones del módulo random para obtener números aleatorios.
        - use slicing de listas para insertar correctamente.
    '''
    # tamanho del padre
    p_size = len(parent1)
    # crear lista de elementos vacios
    child = [None] * p_size
    # hallar indices del primer padre
    start = random.randint(0, p_size - 1)
    end = random.randint(start, p_size - 1)     
    # insertar segmento en el hijo
    child[start:end + 1] = parent1[start:end + 1]
    # crear una lista de elementos restantes para iterar
    remaining = list(range(end + 1, len(parent1))) + list(range(start))
    parent2_r = parent2[end + 1:] + parent2[:end + 1]
    # completar elementos restantes en orden
    for r in remaining:
        for g in parent2_r:
            if g not in child:
                child[r] = g
                parent2_r.remove(g)
                break
    return child

def nextOffspring(population, crossover=orderOneCrossover, elitism=0.0):
    '''
    Generate a new offspring based on given populations. Generate a list of parents 
    to crossover and get 2 childs for each pair.
    Assumes population is ordered.

    returns a new population corresponding to the offspring
    '''
    n_elite = int(len(population) * elitism)

    # print(f'elite: {n_elite}')
    elite_candidates = []
    new_population = []
    if n_elite == 0:
        new_population = population
    else:
        elite_candidates = population[:n_elite]
        new_population = population[:-n_elite]

    # print(f'total pop: {len(elite_candidates)} + {len(new_population)}')
    # make pairs
    
    parents = [(new_population[i], new_population[i + 1]) for i in range(len(new_population) // 2)]
    
    offspring = []
    for parent1, parent2 in parents:
        # get first child
        child1 = crossover(parent1, parent2)
        offspring.append(child1)

        # repeat second child 
        child2 = crossover(parent2, parent1)
        offspring.append(child2)

    # odd number of parents, crossover the last 2 ones once
    if len(new_population) % 2:
        parent1 = new_population[-1]
        parent2 = new_population[-2]
        
        child1 = crossover(parent1, parent2)
        offspring.append(child1)

    return elite_candidates + offspring

def insertMutation(candidate):
    print('mutacion insert')
    print(f'candidato entrante: {candidate}')
    new_candidate = candidate.copy()                # [3, 6, 2, 1, 7, 4, 8, 0, 5]
    i1 = random.randint(0, len(candidate) - 1)      # 3  c[3] => 1
    i2 = random.randint(i1, len(candidate) - 1)     # 6  c[6] => 8
    second = candidate[i2]          # 8
    # remove and insert the second after the first
    new_candidate.remove(second)                    # [3, 6, 2, 1, 7, 4, 0, 5]
    new_candidate.insert(i1 + 1, second)            # [3, 6, 2, 1, 8, 7, 4, 0, 5]
    print(f'candidato mutante: {new_candidate}')
    return new_candidate

def swapMutation(candidate):
    print('mutacion swap')
    print(f'candidato entrante: {candidate}')
    new_candidate = candidate.copy()                # [3, 6, 2, 1, 7, 4, 8, 0, 5]
    i1 = random.randint(0, len(candidate) - 1)      # i1 = 2 c[2] = 2
    i2 = random.randint(i1, len(candidate) - 1)     # i2 = 5 c[5] = 4
    # swap the 2 elements
    aux = new_candidate[i1]                         # aux = 2
    new_candidate[i1] = new_candidate[i2]           # [3, 6, 4, 1, 7, 4, 8, 0, 5]
    new_candidate[i2] = aux                         # [3, 6, 4, 1, 7, 2, 8, 0, 5]
    print(f'candidato mutante: {new_candidate}')
    return new_candidate

def mutate(population, mutation=swapMutation, prob=0.10):
    new_population = []
    for c in population:
        if random.random() < prob:
            new_population.append(mutation(c))
        else:
            new_population.append(c)

    return new_population

