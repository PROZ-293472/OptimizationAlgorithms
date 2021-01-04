library(hash)

is_empty <- function(x) return(length(x) ==0 )


reflection <- function(x, bounds, breach_info){
    if(breach_info == 1) return(bounds[2] - (x - bounds[2]))
    if(breach_info == -1) return(bounds[1] + (bounds[1] - x))
}

wrapping <- function(x, bounds, breach_info){
    if(breach_info == 1) return(bounds[1] + (x - bounds[2]))
    if(breach_info == -1) return(bounds[2] - (bounds[1] - x))
}

projection <- function(x, bounds, breach_info){
    if(breach_info == 1) return(bounds[2])
    if(breach_info == -1) return(bounds[1])
}


repair_methods <- hash()
repair_methods['reflection'] <- reflection
repair_methods['wrapping'] <- wrapping
repair_methods['projection'] <- projection

check_coordinate <- function(x, bounds){
    if(x > bounds[2]) return(1)
    else if(x < bounds[1]) return(-1)
    else return(0)
}



ObjectiveFunction <- setRefClass("ObjectiveFunction",
    fields = list(
        fun = "function",
        dim = "numeric",
        bounds= "list",
        repair_method = "character"),
    methods = list(
        evaluate = function(x){
            return(fun(x))
        },

        compare = function(x,y){
            if(x$fitness > y$fitness){
                return(1)
            }else if(x$fitness < y$fitness){
                return(-1)
            }else{
                return(0)
            }
        },

        repair_population = function(population){
            r_method <- repair_methods[[repair_method]]
            
            for(i in 1:nrow(population)) {
                CHANGED <- FALSE
                row <- population[i,]
                bound_index <- 0
                for(name in names(population)){
                    if(name == 'fitness') break
                    
                    x <- population[i, name] 
                    bound_index <- bound_index + 1
                    current_bounds <- bounds[[bound_index]]
                    
                    while(check_coordinate(x, current_bounds)!=0){
                        CHANGED <- TRUE
                        breach_info <- check_coordinate(x, current_bounds)
                        x <- r_method(x, current_bounds, breach_info)
                    }
                    population[i, name] <- x
                }
                stopifnot(bound_index == dim)
                if(CHANGED){
                    population[i,]$fitness <- evaluate(population[i,1:dim])
                }
            }
            return(population)    
        }

    )
)



Algorithm <- setRefClass("Algorithm",
    fields = list(
       objective_fun = "ObjectiveFunction",
       point_dim = "numeric",
       population = "data.frame",
       iterations = "numeric",
       plot_data = 'logical' ,
       max_iter = "numeric",
       first_pops = 'list',
       tolerance='numeric'
    ),

    methods = list(
        gen_random_population = function(size=50, scaler=1, mean=numeric(point_dim)){
            coordinates <- mean +  scaler * replicate(size, runif(n = point_dim, min = -1, max = 1))
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
            if(dim(min_point)[1] > 1){
                min_point <- min_point[1,]
            }
            # return(as.numeric(min_point[-length(min_point)]))
            return(min_point)
        },
        draw_first_pops = function(){
            max_x1 <- -Inf
            max_x2 <- -Inf
            min_x1 <- Inf
            min_x2 <- Inf
            for(p in first_pops){
                if(max(p['X1']) > max_x1){
                    max_x1 <- max(p['X1'])
                }
                if(max(p['X2']) > max_x2){
                    max_x2 <- max(p['X2'])
                } 
                if(min(p['X1']) < min_x1){
                    min_x1 <- min(p['X1'])
                }
                if(min(p['X2']) < min_x2){
                    min_x2 <- min(p['X2'])
                } 
            }
            border_x1 <- 0.05 *(max_x1 - min_x1)
            border_x2 <- 0.05 *(max_x2 - min_x2)

            colors <- c("#CCCC00", "#FFCC00", "#FF6600", "#FF0000", "#FF66CC", "#9900CC", "#6600CC", "#3333FF", "#33CCFF", "#33FF99", "#00FF00", "#3333FF", "#CCFF99")

            plot.new()
            plot.window(xlim=c(min_x1-border_x1, max_x1+border_x1), ylim=c(min_x2-border_x2, max_x2+border_x2))

            axis(1)
            axis(2)
            box()
            color_index <- 7
            for(i in 1:length(first_pops)){
                color_index <- (color_index)%%length(colors) + 1
                points(first_pops[[i]][,names(p)!='fitness'], cex = 1.1, col=colors[color_index], pch=20)
            }
        }
    )
)

# setClass("Result", slots=list(best_point="data.frame", end_reason="character", mean_iteration_time="numeric", iterations="numeric"))
setClass("Result", slots=list(best_point="data.frame", end_reason="character", mean_iteration_time="numeric", iterations="numeric", times_list='numeric'))
