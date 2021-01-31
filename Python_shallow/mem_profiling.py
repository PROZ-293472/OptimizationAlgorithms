import os
from matplotlib import pyplot as plt


dims = [200]

out_dir = 'C:\\Users\\Lenovo\\Desktop\\Studia\\INZYNIERKA\\OptimizationAlgorithms\\Common'
r_dir = 'C:\\Users\\Lenovo\\Desktop\\Studia\\INZYNIERKA\\OptimizationAlgorithms\\R_shallow'
py_dir = 'C:\\Users\\Lenovo\\Desktop\\Studia\\INZYNIERKA\\OptimizationAlgorithms\\Python_shallow'

alg = 'des'

for dim in dims:
    os.chdir(py_dir)
    os.system(f'mprof run single_eval.py {alg} {dim}')
    os.system(
        f"mprof plot -t '{alg.upper()}_{dim}' -o {out_dir}\\figs\\py_mem_prof_{alg}_{dim}.png")
    os.system(f'mprof clean')

    os.system('PAUSE')
