setwd('C:\\Users\\Lenovo\\Desktop\\Studia\\INZYNIERKA\\OptimizationAlgorithms\\R_shallow')

source("Main.R")
source("TargetFunctions.R")


area <- c(-100,100)
tf <- sum_of_squares

for(algorithm in c('cmaes', 'de', 'des')){
    results <- c()
    for(dimension in seq(2, 70, by=2)){
        rand_points_times <- c()
        max_iter <- 500
        for(i in 1:max_iter){
            point <- runif(dimension, min=area[1], max=area[2])
            start_time <- Sys.time()
            tf(point)
            rand_points_times[i] = as.numeric(Sys.time() - start_time, units="secs")
        }
        mean_rand_point_times <- sum(rand_points_times)/length(rand_points_times)
        print(mean_rand_point_times)

        res <- optimize(objective_function=tf, problem_dimension=dimension, algorithm='cmaes', max_iter=max_iter)
        results <- append(results, c(dimension, (res@mean_iteration_time-mean_rand_point_times)))
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

