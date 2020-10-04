
class ObjectiveFunction:

    def __init__(self, fun, bounds):
        self.bounds = bounds  # 2D array. bounds[i][0] contains upper bound, bounds[i][1] - lower
        self.fun = fun

    def eval(self, x):
        # x - vector
        return self.fun(x)

    def compare(self, x, y):
        # x,y - points
        if x.value > y.value:
            return 1
        elif x.value < y.value:
            return -1
        else:
            return 0

    def check_bounds(self, x):
        # x - vector
        if self.bounds:
            assert len(x) == len(self.bounds)
            for i in range(len(x)):
                if x[i] > self.bounds[i][0] or i < self.bounds[i]:
                    return False
            return True
