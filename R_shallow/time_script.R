setwd('C:\\Users\\Lenovo\\Desktop\\Studia\\INZYNIERKA\\OptimizationAlgorithms\\R_shallow')

source("Main.R")
source("TargetFunctions.R")


area <- c(-100,100)
tf <- sum_of_squares
results <- c()

for(dimention in seq(5, 20, by=5)){
    rand_points_times <- c()
    max_iter <- 400
    for(i in 1:max_iter){
        point <- runif(dimention, min=area[1], max=area[2])
        start_time <- Sys.time()
        tf(point)
        rand_points_times[i] = as.numeric(Sys.time() - start_time, units="secs")
    }
    mean_rand_point_times <- sum(rand_points_times)/length(rand_points_times)
    print(mean_rand_point_times)

    res <- optimize(objective_function=tf, problem_dimention=dimention, algorithm='cmaes', max_iter=max_iter)
    results <- append(results, res)
    print(res)
}
print(results)
