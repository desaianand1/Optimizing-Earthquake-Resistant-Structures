import settings
import random as rand
import simulation as sim

rand.seed(settings.SEED - 1)


# This file provides tools that build the environment. Used in main.py


# Produces a block with three random block dimensions. Used to initialize population
def get_random_block_dimensions():
    # Computing block dimensions
    dimensions = []
    length = rand.uniform(0, 1)
    width = rand.uniform(0, 1)
    height = rand.uniform(0, 1)
    smallest = min([length, width, height])
    ratio = [length / smallest, width / smallest, height / smallest]
    factor = pow((settings.BLOCK_VOLUME / (ratio[0] * ratio[1] * ratio[2])), 1 / 3)
    dimensions.append(ratio[0] * factor)  # length
    dimensions.append(ratio[1] * factor)  # width
    dimensions.append(ratio[2] * factor)  # height
    return dimensions


# creates the initial population. is called at the start of every trial
def initialize_population(env_level):
    pop = []
    for agent_num in range(settings.POPULATION_SIZE):
        structure_traits = []
        for block_num in range(settings.NUM_BLOCKS):
            block_traits = get_random_block_dimensions()
            block_traits.append(settings.STRUCTURE_MASS / 4)
            structure_traits.append(block_traits)
        pop.append([structure_traits, simulate_fitness(structure_traits, -1, 1, env_level)])
    return pop


# fitness will return the fitness value of the building
def simulate_fitness(traits, trial, gen, difficulty_level):
    candidate = sim.run_sim(traits, trial, gen, difficulty_level)
    return candidate[0]


# Assuming arr of size 3, change all dimensions by a GRV
def mutate_block(block_traits):
    output = [-1, -1, -1]
    length_width_or_height = rand.randint(0, 2)  # choose to mutate either l, w, or h
    grv = rand.gauss(0, .5)  # mutation factor
    if grv < -1:
        grv = -.99
    elif grv > 1:
        grv = .99
    mutation_value = grv + 1

    remaining_dimensions = []
    if length_width_or_height == 0:
        remaining_dimensions = [1, 2]
    elif length_width_or_height == 1:
        remaining_dimensions = [0, 2]
    elif length_width_or_height == 2:
        remaining_dimensions = [0, 1]

    output[length_width_or_height] = block_traits[length_width_or_height] * mutation_value
    output[remaining_dimensions[0]] = block_traits[remaining_dimensions[0]] / pow(mutation_value, 0.5)
    output[remaining_dimensions[1]] = block_traits[remaining_dimensions[1]] / pow(mutation_value, 0.5)
    # print("Volume: " + str(output[0] * output[1] * output[2]))
    return output


# returns a 2d array of mutated children, in the same form of parent_population
def get_offspring(parent_population, trial, gen, env_level):
    offspring_population = []
    for parent in parent_population:
        # print("parent")
        # print(parent)
        child_traits = [mutate_block(parent[0][0]), mutate_block(parent[0][1]), mutate_block(parent[0][2]),
                        mutate_block(parent[0][3])]
        fitness = simulate_fitness(child_traits, trial, gen, env_level)
        child_to_add = [child_traits, fitness]
        offspring_population.append(child_to_add)
    return offspring_population
