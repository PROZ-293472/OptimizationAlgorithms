rm(list = ls())
setwd('C:\\Users\\Lenovo\\Desktop\\Studia\\INZYNIERKA\\OptimizationAlgorithms\\R_shallow')

source("Main.R")
source("TargetFunctions.R")


area <- c(-100,100)
tf <- rastrigin
lbd <- 100

for(algorithm in c('des')){
    print(algorithm)
    results <- c()
    for(dimension in seq(2, 70, by=2)){
        print(dimension)
        max_iter <- 300

        total_rand_point_time <- 0
        for(j in 1:lbd){
            rand_points_times <- c()
            for(i in 1:max_iter){
                point <- runif(dimension, min=area[1], max=area[2])
                start_time <- Sys.time()
                tf(point)
                rand_points_times[i] = as.numeric(Sys.time() - start_time, units="secs")
            }
            mean_rand_point_times <- sum(rand_points_times)/length(rand_points_times)
            total_rand_point_time <- total_rand_point_time + mean_rand_point_times
        }
        print(total_rand_point_time)


        res <- optimize(objective_function=tf, problem_dimension=dimension, algorithm=algorithm, max_iter=max_iter)
        results <- append(results, c(dimension, (res@mean_iteration_time-total_rand_point_time)))
        print(res@mean_iteration_time-total_rand_point_time)
    }
    results <- matrix(results, ncol=2, byrow=TRUE)
    print(results)
    df <- data.frame(results)
    colnames(df) <- c('Dim', 'R')

    fname <- paste('r_mean_time_per_dim_', algorithm, sep='')
    fname <- paste(fname, '.csv', sep='')
    path <- paste("C:\\Users\\Lenovo\\Desktop\\Studia\\INZYNIERKA\\OptimizationAlgorithms\\Common\\", fname, sep="")

    write.csv(df,path, row.names = FALSE)
}

