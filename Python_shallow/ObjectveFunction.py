import numpy as np


class ObjectiveFunction:

    def __init__(self, fun, dim, bounds=None, repair_method=None):
        self.fun = fun
        self.dim = dim
        # 2D array. bounds[i][1] contains upper bound, bounds[i][0] - lower
        self.bounds = bounds

        repair_methods = {
            'wrapping': ObjectiveFunction._wrap,
            'projection': ObjectiveFunction._project,
            'reflection': ObjectiveFunction._reflect
        }
        if repair_method:
            self.repair_method = repair_methods[repair_method]

        if self.bounds:
            assert self.repair_method,  'If bounds are given, please specify repair method'
        # assert (self.repair_method and self.bounds) or (
        #     not self.repair_method and not self.bounds), 'Both bounds and repair method must be specified'

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

    def _check_bounds(self, point):
        # x - vector
        x = point.coordinates
        if self.bounds:
            assert len(x) == len(self.bounds)
            # out_info is a list of tuples where first element is an index of breached bound and second - info if it's upper or lower bound
            out_info = []
            for i in range(len(x)):
                if x[i] < self.bounds[i][0]:
                    out_info.append((i, 0))
                elif x[i] > self.bounds[i][1]:
                    out_info.append((i, 1))
            return out_info

    def repair_point(self, point):
        assert self.bounds is not None, 'No bounds specified!'
        breach_info = self._check_bounds(point)
        for bi in breach_info:
            coordinate_index, bound_index = bi
            broken_coordinate = point.coordinates[coordinate_index]
            broken_bound = self.bounds[coordinate_index]
            is_upper_bound = bool(bound_index)

            new_coordinate = self.repair_method(
                broken_coordinate, broken_bound, is_upper_bound)
            point.coordinates[coordinate_index] = new_coordinate
        if breach_info:
            point.value = self.eval(point.coordinates)
        return point

    def repair_points(self, points):
        return np.array([self.repair_point(p) for p in points])

    # REPAIR METHODS
    @staticmethod
    def _wrap(coordinate, bounds, is_upper):
        if is_upper:
            return bounds[0] + (coordinate - bounds[1])
        return bounds[1] - (bounds[0] - coordinate)

    @staticmethod
    def _reflect(coordinate, bounds, is_upper):
        if is_upper:
            return bounds[1] - (coordinate - bounds[1])
        return bounds[0] + (bounds[0] - coordinate)

    @staticmethod
    def _project(coordinate, bounds, is_upper):
        if is_upper:
            return bounds[1]
        return bounds[0]

    # def _find_broken_points(self, points):
    #     broken_points = []
    #     for p in points:
    #         breached_bounds_info = self._check_bounds(p)
    #         if not breached_bounds_info:
    #             continue
    #         broken_points.append(
    #             {'point': p, 'breach_info': breached_bounds_info})
    #     return broken_points

    # def _repair_excluding_resampling(self, broken_points_info, method):
    #     def wrap(coordinate, bounds, is_upper):
    #         if is_upper:
    #             return bounds[0] + (coordinate - bounds[1])
    #         return bounds[1] - (bounds[0] - coordinate)

    #     def reflect(coordinate, bounds, is_upper):
    #         if is_upper:
    #             return bounds[1] - (coordinate - bounds[1])
    #         return bounds[0] + (bounds[0] - coordinate)

    #     def project(coordinate, bounds, is_upper):
    #         if is_upper:
    #             return bounds[1]
    #         return bounds[0]

    #     repair_methods = {
    #         'wrapping': wrap,
    #         'reflection': reflect,
    #         # 'resampling': resample,
    #         'projection': project
    #     }

    #     repair_method = repair_methods[method]
    #     repaired_points = []
    #     for point_info in broken_points_info:
    #         point, breach_info = point_info['point'], point_info['breach_info']

    #         for bi in breach_info:
    #             coordinate_index, bound_index = bi
    #             broken_coordinate = point[coordinate_index]
    #             broken_bound = self.bounds[coordinate_index]
    #             is_upper_bound = bool(bound_index)

    #             new_coordinate = repair_method(
    #                 broken_coordinate, broken_bound, is_upper_bound)
    #             point[coordinate_index] = new_coordinate
    #         repaired_points.append(point)
    #     return repaired_points

    # def resample(self, point):
    #     pass

    # def find_and_repair_breached_points(self, points):
    #     broken_points = self._find_broken_points(points)
