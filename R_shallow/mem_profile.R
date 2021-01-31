# devtools::install_github("rstudio/profvis")
rm(list = ls())

setwd('C:\\Users\\Lenovo\\Desktop\\Studia\\INZYNIERKA\\OptimizationAlgorithms\\R_shallow')
source("Main.R")
source("TargetFunctions.R")
library(profvis)


tf <- sphere
max_iter <- 100

args <- commandArgs(trailingOnly=TRUE)

alg <- 'cmaes'
dim <- 200

constr <- list(c(-10,10))
constr <- rep(constr, dim)



res <- profvis({
    optimize(objective_function=tf,
            problem_dimension=dim,
            algorithm=alg,
            max_iter=max_iter,
            constraints=constr,
            repair_method='projection')
            
    }, height = "800px") 


