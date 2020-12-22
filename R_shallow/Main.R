source("CMAES.R")
source("Differential_Evolution.R")
source("Classes.R")
source("Utils.R")
source("TargetFunctions.R")
library(hash)

optimize <- function(objective_function, problem_dimension, constraints=c(), algorithm='cmaes', max_iter=400, repair_method='reflection'){
    algorithms <- hash()
    algorithms['cmaes'] <- CMAES$new()
    algorithms['de'] <- DifferentialEvolution$new()

    alg <- algorithms[[algorithm]]
    if(is_empty(constraints)){
        of <- ObjectiveFunction$new(fun=objective_function, dim=problem_dimension)
    }
    else {
        of <- ObjectiveFunction$new(fun=objective_function, dim=problem_dimension, bounds=constraints, repair_method=repair_method)
    }

    alg$objective_fun <- of
    alg$point_dim <- of$dim
    alg$max_iter <- max_iter
    print(of$dim)
    return(alg$run())
}
objective_function <- sum_of_squares
problem_dimension <- 2
constraints <- list(c(-0.5,0.5), c(-0.2,0.5))
repair_method <- 'projection'
algorithm <- 'cmaes'
res <- optimize(objective_function, problem_dimension, constraints, algorithm, repair_method=repair_method)

