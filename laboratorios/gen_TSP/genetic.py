import random
import math

def initPopulation(cities, pop_size):
    cities_id = [i for i in range(len(cities))]
    population = []
    for i in range(pop_size):
        candidate = cities_id.copy()
        random.shuffle(candidate)
        population.append(candidate)

    return population

def citiesDist(c1, c2, cities):
    'distancia euclidiana entre 2 ciudades'
    pos_c1 = cities[c1]['position']
    pos_c2 = cities[c2]['position']
    
    return math.sqrt((pos_c2[0] - pos_c1[0])**2 + (pos_c2[1] - pos_c1[1])**2)


def cost(candidate, cities):
    'inverse fitness function, you must minimize this'
    total_dist = 0
    for i in range(len(candidate) - 1):
        total_dist += citiesDist(candidate[i], candidate[i + 1], cities)

    return total_dist


def select(population):
    pass

def crossover(population):
    pass

def mutate(population, prob=0.1):
    pass