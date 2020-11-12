ObjectiveFunction <- setRefClass("ObjectiveFunction",
    fields = list(
        fun = "function",
        dim = "numeric",
        bounds= "numeric",
        repair_method = "character"),
    methods = list(
        evaluate = function(x){
            return(fun(x))
        },
        # compare = function(x,y){
        #     if(x$value > y){
        #         return(1)
        #     }else if(x$value < y$value){
        #         return(-1)
        #     }else{
        #         return(0)
        #     }
        # },
        check_bounds = function(x){

        }

    )
)


# Point <- setRefClass("Point",
#     fields = list(
#         coordinates = "numeric",
#         objective_fun = "ObjectiveFunction",
#         bounds= "numeric"),
#     methods = list(
#         evaluate = function(x){
#             return(fun(x))
#         },
#         compare = function(x,y){
#             if(x$value > y$value){
#                 return(1)
#             }else if(x$value < y$value){
#                 return(-1)
#             }else{
#                 return(0)
#             }
#         },
#         check_bounds = function(x){
#         }
#     )
# )


Algorithm <- setRefClass("Algorithm",
    fields = list(
       objective_fun = "ObjectiveFunction",
       point_dim = "numeric",
       population = "data.frame",
       iterations = "numeric",
       plot_data = 'logical' ,
       max_iter = "numeric" 
    ),

    methods = list(
        gen_random_population = function(size=50, scaler=1){
            coordinates <- scaler * replicate(size, runif(n = point_dim, min = -1, max = 1))
            fitness <- c()
            for(i in 1:dim(coordinates)[2]){
                fitness[i]<-objective_fun$evaluate(coordinates[,i])
            }
            population <<- data.frame(t(coordinates), fitness)
        },
        get_population_mean = function(){
            m <- colMeans(population)
            return(m[-length(m)])
        },
        sel_best = function(){
            min_fitness <- min(population[,'fitness'])
            min_point <- population[population['fitness'] == min_fitness,]
            return(as.numeric(min_point[-length(min_point)]))
        }
    )
)

setClass("Result", slots=list(best_point="numeric", end_reason="character", mean_iteration_time="numeric"))