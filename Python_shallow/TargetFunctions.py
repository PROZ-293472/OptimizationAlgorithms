def sum_of_squares(point):
    sum = 0.0
    for p in point:
        sum += p**2
    return sum


def rosenrock(points):
    x = points[0]
    y = points[1]
    #Funcion Rosenbrock en 2D
    return 100 * ((y - (x**2))**2) + ((1 - (x**2))**2)