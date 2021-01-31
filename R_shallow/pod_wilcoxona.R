setwd('C:\\Users\\Lenovo\\Desktop\\Studia\\INZYNIERKA\\OptimizationAlgorithms\\R_shallow')
rm(list = ls())

source('Main.R')
source("TargetFunctions.R")
library(hash)
library(rlist)

tfs <- hash()
tfs['sphere'] <- sphere
tfs['rosenbrock'] <- rosenbrock
tfs['rastrigin'] <- rastrigin

eval_num <- 25
constr_bounds <- c(-1e3,1e3)
constr_handle <- 'projection'

for(fun_name in c('sphere')){
    print(fun_name)
    fun <- tfs[[fun_name]]

    # fixed iterations
    print('ITERATIONS')
    out_dict <- hash()
    for(alg in c('de')){
        print(alg)

        res_df <- data.frame(matrix(ncol = 2, nrow = 0))
        colnames(res_df) <- c("dim", "best_val")
        for(dim in c(3)){
            print(dim)
            # constraints <- rep(list(constr_bounds), dim)
            constraints <- list()

            for(curr_eval in 1:eval_num){
                print(curr_eval)
                res <- optimize(objective_function=fun, 
                                problem_dimension=dim, 
                                algorithm=alg, 
                                max_iter=400, 
                                constraints=constraints, 
                                repair_method=constr_handle)

                new_row <- data.frame(dim, res@best_point['fitness'])
                names(new_row)<-c("dim","best_val")
                res_df <- rbind(res_df, new_row)
            }
        }

        fname <- paste('r_fixed_iter_', fun_name, sep='')
        fname <- paste(fname, alg, sep='_')
        fname <- paste(fname, '_50.csv', sep='')
        path <- paste("C:\\Users\\Lenovo\\Desktop\\Studia\\INZYNIERKA\\OptimizationAlgorithms\\Common\\", fname, sep="")
        write.csv(res_df,path, row.names = FALSE)
    }
}