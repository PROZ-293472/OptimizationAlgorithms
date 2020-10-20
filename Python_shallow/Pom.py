import General as gen
from DifferentialEvolution import DifferentialEvolution
import TargetFunctions as TargetFunctions
from CMAES import CMAES
from ObjectveFunction import ObjectiveFunction

gen.Setup.generate_starting_population(pop_size=30, dim=2, bounds=[
                                       10, 20], filename='temp.csv')

of = ObjectiveFunction(fun=TargetFunctions.sphere, bounds=None, dim=2)

alg = DifferentialEvolution(objective_fun=of, plot_data=True)
# alg = DE.DifferentialEvolution(objective_fun=of,  population_filename='temp.csv', plot_data=False)
alg.run()
print(alg.sel_best().__dict__)
print(alg.end_reason)
