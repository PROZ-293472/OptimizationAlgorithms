import src.General as gen
import src.algorithms.DifferentialEvolution as DE
import mats.TargetFunctions as TargetFunctions
import src.algorithms.CMAES as CMAES
from src.entities.ObjectveFunction import ObjectiveFunction

gen.Setup.generate_starting_population(pop_size=30, dim=2, bounds=[10,20], filename='temp.csv')

of = ObjectiveFunction(fun=TargetFunctions.sum_of_squares, bounds=None)

alg = CMAES.CMAES(objective_fun=of,  population_filename='temp.csv', plot_data=True)
# alg = DE.DifferentialEvolution(objective_fun=of,  population_filename='temp.csv', plot_data=False)
alg.run()
print(alg.sel_best())
print(alg.end_reason)