rm(list = ls())

source("CMAES.R")
source("Differential_Evolution.R")
source('DES.R')
source("Classes.R")
source("Utils.R")
source("TargetFunctions.R")
library(hash)

optimize <- function(objective_function, problem_dimension, constraints=c(), algorithm='cmaes', max_iter=1000, repair_method='reflection', tolerance=0){
    algorithms <- hash()
    algorithms['cmaes'] <- CMAES$new()
    algorithms['de'] <- DifferentialEvolution$new()
    algorithms['des'] <- DES$new()

    alg <- algorithms[[algorithm]]
    if(is_empty(constraints)){
        of <- ObjectiveFunction$new(fun=objective_function, dim=problem_dimension)
    }
    else {
        of <- ObjectiveFunction$new(fun=objective_function, dim=problem_dimension, bounds=constraints, repair_method=repair_method)
    }
    
    alg$tolerance <- tolerance
    alg$objective_fun <- of
    alg$point_dim <- of$dim
    alg$max_iter <- max_iter
    res <- alg$run()
    return(res)
}