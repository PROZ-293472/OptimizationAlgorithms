source("Classes.R")

DEFAULT_CR <- 0.5
DEFAULT_F <- 0.8

is_empty <- function(x) return(length(x) ==0 )

DifferentialEvolution <- setRefClass(
    "DifferentialEvolution",
    contains = "Algorithm",
    fields = list(
        cr = "numeric",
        f = "numeric",
        H = "data.frame",
        init_mean = "numeric"
    ),
    methods = list(
        init_default_parameters = function(){
            if(is_empty(f)){
                f <<- DEFAULT_F
            }
            if(is_empty(cr)){
                cr <<- DEFAULT_CR
            }
        },
        crossover = function(x,y){
            z <- c()
            for (i in 1:length(x)){
                a <- runif(1, 0, 1)
                if (a < cr) 
                z <- append(z, y[i])
                else 
                z <- append(z, x[i])
            }
            return(z)
        },

        tournanemt = function(x,y){
            cond <- x['fitness'] > y['fitness']
            if(cond) 
                return(y)
            else
                return(x)
        },

        run = function() {
            init_default_parameters()
            if(is_empty(init_mean)){
                gen_random_population()
            }else{
                gen_random_population(mean=init_mean)
            }
            

            if(point_dim == 2){
                LOG_POPS <- TRUE
                first_pops <<- list(population) 
            }else{
                LOG_POPS <- FALSE
            }

            H <<- population
            mi <- dim(population)[1]
            mean_time <- 0
            iterations <<- 0
            best_point <- sel_best()
            times_vec <- c()
            max_mem <- 0
            while(iterations < max_iter && objective_fun$evaluate(best_point) > tolerance){
                if(memory.size()>max_mem){
                    max_mem <- memory.size()
                }
                start_time <- Sys.time()
                if(LOG_POPS && iterations <20){
                    first_pops <<- list.append(first_pops, population)
                }

                next_P <- population
                for (i in 1:mi){
                    indexes <- sample(1:mi, 3, replace=F)
                    r <- as.matrix(population[indexes[1],-length(population)])
                    d_e <- as.matrix(population[indexes[2:3],-length(population)])
                    
                    M <- r + f*(d_e[2,] - d_e[1,])
                    cross <- crossover(r, M)
                    O <- data.frame(t(cross), fitness=objective_fun$evaluate(cross))
                    if(!is_empty(objective_fun$bounds)){
                        O <-objective_fun$repair_population(O)
                    }
                
                    next_P[i,] <- tournanemt(population[i,], O)
                }
                population <<- next_P
                population_best <- sel_best()
                if(population_best$fitness < best_point$fitness){
                    best_point <- population_best
                }
                times_vec[iterations] <- (Sys.time() - start_time)
                iterations <<- iterations+1
            }
            mean_time <- sum(times_vec)/iterations
            mean_time <- as.numeric(mean_time, units="secs")
            print(max_mem)
            return(new('Result', best_point=best_point, end_reason='max_iter',mean_iteration_time=mean_time, iterations=iterations))
        }
    )
)