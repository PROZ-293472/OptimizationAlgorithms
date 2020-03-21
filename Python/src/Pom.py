import numpy as np
import OptimizationAlgorithms.Python.src.General as gen
import OptimizationAlgorithms.Python.src.DifferentialEvolution as DE
import OptimizationAlgorithms.Python.mats.TargetFunctions as TargetFunctions
from OptimizationAlgorithms.Python.src.ObjectveFunction import ObjectiveFunction

gen.Setup.generate_starting_population(pop_size=30, dim=3, bounds=[10,20], filename='temp.csv')

of = ObjectiveFunction(fun=TargetFunctions.sum_of_squares, bounds=None)

alg = DE.DifferentialEvolution(objective_fun=of,
                               population_filename='temp.csv')

alg.run()
print(alg.sel_best())
print(alg.end_reason)