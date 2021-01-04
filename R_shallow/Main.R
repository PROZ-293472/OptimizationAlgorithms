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
    # alg$defaultMean <- c(1,1)
    # alg$m <- c(1,1)
    # alg$init_mean <- c(1,1)
    res <- alg$run()
    # print(alg$first_pops)
    # alg$draw_first_pops()
    return(res)
}

# objective_function <- reastrigin
# problem_dimension <- 2
# # constraints <- list(c(-0.5,0.5), c(-0.2,0.5))
# constraints <- list(c(-Inf,Inf), c(-Inf,Inf))
# repair_method <- 'projection'
# algorithm <- 'des'
# res <- optimize(objective_function, problem_dimension, constraints, algorithm, repair_method=repair_method, tolerance=1e-100, max_iter=500)

# objective_function <- sum_of_squares
# problem_dimension <- 70
# repair_method <- 'projection'
# algorithm <- 'de'
# for(algorithm in c('cmaes', 'des')){
#     reps <- 10
#     res_list <- list()
#     for(i in 1:reps){
#         print(i)
#         res <- optimize(objective_function, problem_dimension, constraints=c(), algorithm, repair_method=repair_method, tolerance=1e-100, max_iter=1000)
#         res_list <- list.append(res_list,res)
#     }

#     i <- 0
#     for(r in res_list){
#         if(i==0){
#             out <- r@times_list
#             i <- 1
#         }else{
#             out <- out + r@times_list
#         }
#     }
#     R <- out/reps
#     df <- data.frame(R)
#     fname <- paste(algorithm, '_iter_time.csv', sep='')
#     path <- paste("C:\\Users\\Lenovo\\Desktop\\Studia\\INZYNIERKA\\OptimizationAlgorithms\\Common\\", fname, sep="")
#     write.csv(df,path, row.names = FALSE)
# }