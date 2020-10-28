source("CMAES.R")
source("Differential_Evolution.R")
source("Classes.R")
source("Utils.R")
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
    return(alg$run())
}


sum_of_squares<-function(point){
   sum <- 0.0        
   for(p in point)
   {
     sum <- sum + p^2
   }
   return(sum)
}
