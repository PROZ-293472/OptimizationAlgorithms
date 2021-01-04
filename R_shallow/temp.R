rm(list = ls())
source("Main.R")
source("TargetFunctions.R")
library(rlist)

switch <- 'fixed_iter'
of <- rosenbrock

for(dim in c(3,5,10,20,50,70)){
    res_list <- list()
    for(alg in c('de', 'cmaes', 'des')){
        if(switch == 'fixed_iter'){
            res <- optimize(objective_function=of, problem_dimension=dim, , algorithm=alg, max_iter=400)
            res_list <- list.append(res_list, res)
        }else if (switch == 'fixed_tol') {
            res <- optimize(objective_function=of, problem_dimension=dim, , algorithm=alg, tolerance=1e-6)
            res_list <- list.append(res_list, res)
        } 
    }
    # print(res_list)
    str_2_print <- toString(dim)
    for(r in res_list){
        str_2_print <- paste(str_2_print,' & $\num{', sep="")

        if(switch=='fixed_iter'){
            fit <- r@best_point['fitness']
            str_2_print <- paste(str_2_print, toString(fit), sep="")

        }else if(switch == 'fixed_tol'){
            iter <- r@iterations
            str_2_print <- paste(str_2_print, toString(iter), sep="")
        }

        str_2_print <- paste(str_2_print,'}$', sep="")
    }
    str_2_print <- paste(str_2_print,'\\', sep="")
    print(str_2_print)
}
