class Point:

    def __init__(self, coordinates, objective_fun):
        self.coordinates = coordinates
        self.value = objective_fun.eval(self.coordinates)
        self.is_acceptable = objective_fun.check_bound(self.coordinates)



