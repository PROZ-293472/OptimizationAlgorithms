library(pracma)
library(comprehenr)
library(rlist)
source("Classes.R")

is_empty <- function(x) return(length(x) ==0 )
DEFAULT_SIGMA <- 0.3

CMAES <- setRefClass(
    "CMAES",
    contains = "Algorithm",
    fields = list(
        m = "numeric",
        sigma = "numeric",
        lambda = "numeric",
        mu = "numeric",
        weights = "numeric",
        mu_w = "numeric",
        cc = "numeric",
        cs = "numeric",
        c1 = "numeric",
        cmu = "numeric",
        d_s = "numeric",
        chiN = "numeric"
    ),
    methods = list(
        init_default_parameters = function(){
            if(is_empty(population)){
                population <<- gen_random_population()
            }
            if(is_empty(m)){
                m <<- get_population_mean()
            }
            if(is_empty(sigma)){
                sigma <<- DEFAULT_SIGMA
            }
            if(is_empty(lambda)){
                lambda <<- dim(population)[1]
            }
            if(is_empty(mu)){
                mu <<- floor(lambda/2)
            }
            if(is_empty(weights)){
                tmp <- log(mu + 1/2) - to_vec(for(i in 1:mu) log(i))
                weights <<- tmp/sum(tmp)
            }
            if(is_empty(mu_w)){
                mu_w <<- sum(weights**2)**(-1)
            }
            if(is_empty(cc)){
                cc <<- (4 + mu_w/point_dim) / (point_dim + 4 + 2*mu_w/point_dim)
            }
            if(is_empty(cs)){
                cs <<- (mu_w + 2) / (point_dim + mu_w + 5)
            }
            if(is_empty(c1)){
                c1 <<- 2 / ((point_dim + 1.3)**2 + mu_w)
            }
            if(is_empty(cmu)){
                cmu <<- min(1-c1 , 2*(mu_w-2 + 1/mu_w) / ((point_dim + 2)**2 + mu_w))
            }
            if(is_empty(d_s)){
                d_s <<- 1 + 2*max(0, sqrt((mu_w - 1)/(point_dim + 1)) - 1) + cs
            }
            if(is_empty(chiN)){
                chiN <<- point_dim**0.5 * (1-1/(4*point_dim)+1/(21*point_dim**2))
            }
        },

        generate_population = function(C){
            generated_pop <- m + sigma*MASS::mvrnorm(lambda, mu = numeric(point_dim), Sigma = C)
            fitness <- to_vec(for(i in 1:dim(generated_pop)[1]) + objective_fun$evaluate(generated_pop[i,]))
            population_raw<-data.frame(generated_pop, fitness)
            if(!is_empty(objective_fun$bounds)){
                population<<-objective_fun$repair_population(population_raw)
            }else{
                population <<- population_raw
            }
            # # DEBUG !
            # plot(population[,1], population[,2], pch = 19)
            # Sys.sleep(2)
        },

        sort_by_fitness = function() {
            return(population[order(population['fitness'], decreasing=FALSE),])
        },

        run = function() {
            init_default_parameters()

            if(point_dim == 2){
                LOG_POPS <- TRUE
                first_pops <<- list(population) 
            }else{
                LOG_POPS <- FALSE
            }
            iterations <<- 0

            pc <- numeric(point_dim)
            ps <- numeric(point_dim)
            B <- eye(point_dim)                       
            D <- ones(point_dim , 1 ) 
            # C <- B %*% diag(D^2) %*% t(B)           
            # invsqrtC <- B %*% diag(D^(-1)) %*% t(B)   
            C <- eye(point_dim)
            invsqrtC <- eye(point_dim)
            mean_time <- 0
            times_vec <- c()
            best_point <- sel_best()
            while(iterations < max_iter && objective_fun$evaluate(best_point) > tolerance){
                start_time <- Sys.time()

                generate_population(C)
                if(LOG_POPS && iterations <20){
                    first_pops <<- list.append(first_pops, population)
                }
                pop_sorted <- sort_by_fitness()
#                 print(pop_sorted)
                pop_sorted <- as.matrix(pop_sorted[-length(pop_sorted)])
                new_m <- t(pop_sorted)[,1:mu] %*% weights
                ps <- (1-cs)*ps + sqrt(cs*(2-cs)*mu_w) * invsqrtC %*% (new_m-m) / sigma
                HIGH_SIGMA <- norm(ps)/sqrt(1-(1-cs)^(2*iterations/lambda))/chiN < 1.4 + 2/(point_dim+1)
                pc <- (1-cc)*pc + HIGH_SIGMA * sqrt(cc*(2-cc)*mu_w) * (new_m-m) / sigma
                artmp <- (1/sigma) * (t(pop_sorted)[,1:mu] - matrix(rep(m,mu), point_dim, mu))
                C <- (1-c1-cmu) * C + c1*(pc%*%t(pc) + (1-HIGH_SIGMA)*cc*(2-cc)*C) + cmu * artmp %*% diag(weights) %*% t(artmp)
                sigma <<- sigma * exp((cs/d_s)*(norm(ps)/chiN - 1))
                
                best_point <- sel_best()
                # print(best_point)
#                 print(sel_best())
                    
                C_upper <- C
                C_upper_diag <- C
                u <- lower.tri(C, diag = TRUE)
                u_d <-  lower.tri(C, diag = FALSE)
                C_upper[u] <- 0
                C_upper_diag[u_d] <- 0
                C <- C_upper_diag + t(C_upper)
                eig <- eigen(C)
                D <- eig$values
                B <- eig$vectors
                D <- sqrt(D)
                invsqrtC <- B %*% diag(D^-1) %*% t(B)
                m <<- c(new_m)
                iterations <<- iterations+1

                times_vec[iterations] <- (Sys.time() - start_time)
                # mean_time <- times_vec[iterations]
            }
            mean_time <- sum(times_vec)/iterations
            mean_time <- as.numeric(mean_time, units="secs")
            return(new('Result', best_point=best_point, end_reason='max_iter',mean_iteration_time=mean_time, iterations=iterations, times_list=times_vec))
        }
    )
)