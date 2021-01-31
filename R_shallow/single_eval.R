setwd('C:\\Users\\Lenovo\\Desktop\\Studia\\INZYNIERKA\\OptimizationAlgorithms\\R_shallow')

source("TargetFunctions.R")
source("Main.R")

tf <- sphere
max_iter <- 200

args <- commandArgs(trailingOnly=TRUE)

alg <- 'cmaes'
dim <- 6

constr <- list()

res <- optimize(objective_function=tf,
        problem_dimension=dim,
        algorithm=alg,
        max_iter=max_iter,
        constraints=constr,
        repair_method='projection')