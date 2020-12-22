import os
from matplotlib import pyplot as plt


dims = [2, 5, 10, 20, 50, 100, 200, 500]

dir_ = 'C:\\Users\\Lenovo\\Desktop\\Studia\\INZYNIERKA\\OptimizationAlgorithms\\Python_shallow'

os.chdir(dir_)

for dim in dims:
    os.system(f'mprof run single_eval.py {dim}')
    os.system(f'mprof plot -o {dir_}\\figs\\de_{dim}.png')
    os.system(f'mprof clean')
