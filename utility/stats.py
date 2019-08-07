import settings as set
import random as rand
rand.seed(set.SEED)


# Returns a list with the current gen, min, avg, and max
def get_stats(pop, gen):
    print(pop)
    least_fit = pop[0][1]
    most_fit = pop[0][1]
    best_traits = []
    avg = 0
    for element in pop:
        if element[1] < least_fit:
            least_fit = element[1]
        if element[1] > most_fit:
            most_fit = element[1]
            best_traits = element[0]
        avg += element[1]
    avg /= set.POPULATION_SIZE
    return [gen, least_fit, avg, most_fit, best_traits]


def fitness_key(agent):
    return agent[1]




