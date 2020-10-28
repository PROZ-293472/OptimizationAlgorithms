source("Main.R")

area <- c(-100,100)
tf <- sum_of_squares
results <- c()

for(dim in seq(5, 40, by=5)){
    rand_points_times <- c()
    max_iter <- max(1e5, dim*1e4)
    for(i in 1:max_iter){
        point <- runif(dim, min=area[1], max=area[2])
        start_time = Sys.time()
        tf(point)
        rand_points_times[i] = as.numeric(Sys.time() - start_time, units="secs")
    }
    mean_rand_point_times <- sum(rand_points_times)/length(rand_points_times)
    print(mean_rand_point_times)
}