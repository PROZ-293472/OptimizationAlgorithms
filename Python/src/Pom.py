import numpy as np
import OptimizationAlgorithms.Python.src.General as gen
import OptimizationAlgorithms.Python.src.DifferentialEvolution as DE
import OptimizationAlgorithms.Python.mats.TargetFunctions as TargetFunctions

gen.Setup.generate_starting_population(dim=3, bounds=[0,3], filename='temp.csv')

alg = DE.DifferentialEvolution(TargetFunctions.sum_of_squares,
                               population_filename='temp.csv')

alg.run()
print(alg.sel_best())