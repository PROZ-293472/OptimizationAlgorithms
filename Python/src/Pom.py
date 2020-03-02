import  numpy as np
from src import General as gn

bounds = [2,30]
dim = 2

# points = np.random.uniform(low=bounds[0], high=bounds[1], size=(50, dim))
# np.savetxt('temp.csv', points, delimiter=',')
#
# print(np.genfromtxt('temp.csv', delimiter=','))

gn.General.generate_starting_population(dim, bounds, 'temp2.csv')
print(gn.General.read_staring_population('temp2.csv'))
