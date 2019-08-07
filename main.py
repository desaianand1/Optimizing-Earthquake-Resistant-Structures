import csv
from utility import stats
import settings
import evolution_tools as tools

best_traits = []

# experiment loop
for trial in range(1, settings.NUM_TRIALS + 1):
    file_name = "./data/" + settings.EXP_NAME + "_" + str(settings.FITNESS_FUNCTION) + "_trial_" + str(trial)
    with open(file_name + ".csv", 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["Gen", "Min", "Avg", "Max"])
        # generation loop
        difficulty_level = settings.INIT_ENV_LEVEL
        population = tools.initialize_population(difficulty_level)
        goal_fitness = settings.FITNESS_INTERVAL
        for gen_num in range(1, settings.MAX_GEN + 1):
            offspring = tools.get_offspring(population, trial, gen_num, difficulty_level)
            offspring_and_parents = sorted(population + offspring, key=stats.fitness_key)
            population = offspring_and_parents[settings.POPULATION_SIZE:]
            population_stats = stats.get_stats(population, gen_num)
            avg_fitness = population_stats[2]
            print("AVG: " + str(avg_fitness))
            # Increase the difficulty and set a new goal
            if avg_fitness > goal_fitness:
                goal_fitness += settings.FITNESS_INTERVAL
                difficulty_level += 1

            print("Trial: " + str(trial) + " Generation: " + str(gen_num))
            print("best traits:" + str(population_stats[4]))
            writer.writerow(population_stats[0:4])
            best_traits.append(population_stats[4])
    file_2 = "./data/" + settings.EXP_NAME + "_" + str(settings.FITNESS_FUNCTION) + "_best_trait_" + str(trial)
    with open(file_2 + ".csv", 'w', newline='') as csvfile2:
        writer2 = csv.writer(csvfile2, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer2.writerow(
            ["Block0 X", "Block0 Y", "Block0 Z", "Mass0", "Block1 X", "Block1 Y", "Block1 Z", "Mass1", "Block2 X",
             "Block2 Y", "Block2 Z", "Mass2",
             "Block3 X", "Block3 Y", "Block3 Z", "Mass3"])
        for trait in best_traits:
            print("trait from best_trait: " + str(trait))
            writer2.writerow(trait)
