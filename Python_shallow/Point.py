class Point:

    # during the creation of object, there's an evaluation of objective function hence it's done once
    def __init__(self, coordinates, objective_fun=None):
        self.coordinates = coordinates
        if objective_fun:
            self.defined = True
            self.value = objective_fun.eval(self.coordinates)
            # self.is_acceptable = objective_fun.check_bounds(self.coordinates)
        else:
            self.defined = False

    def update(self, objective_fun):
        if not self.defined:
            self.value = objective_fun.eval(self.coordinates)
            # self.is_acceptable = objective_fun.check_bounds(self.coordinates)
