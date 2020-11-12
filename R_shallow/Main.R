source("CMAES.R")
source("Differential_Evolution.R")
source("Classes.R")
source("Utils.R")
source("TargetFunctions.R")
library(hash)

optimize <- function(objective_function, problem_dimention, constraints=c(), algorithm='cmaes', max_iter=400){
algorithms <- hash()
algorithms['cmaes'] <- CMAES$new()
algorithms['de'] <- DifferentialEvolution$new()

alg <- algorithms[[algorithm]]
if(is_empty(constraints)){
    of <- ObjectiveFunction$new(fun=objective_function, dim=problem_dimention)
}
else {
    of <- ObjectiveFunction$new(fun=objective_function, dim=problem_dimention, bounds=constraints)
}

alg$objective_fun <- of
alg$point_dim <- of$dim
alg$max_iter <- max_iter
print(of$dim)
return(alg$run())
}



