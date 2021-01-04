library(pracma)
library(comprehenr)
library("ringbuffer")
source("Classes.R")

is_empty <- function(x) return(length(x) ==0 )

DES <- setRefClass(
    "DES",
    contains = "Algorithm",
    fields = list(
        defaultMean = "numeric",
        lambda = "numeric",
        mu = "numeric",
        mueff = "numeric",
        cc = "numeric",
        pathLength = "numeric",
        Ft = "numeric",
        c_Ft = "numeric",
        cp = "numeric",
        weights = "numeric",
        weightsPop = "numeric",
        pathRatio = "numeric",
        histSize = "numeric"
    ),
    methods = list(
        init_default_parameters = function(){
            if(is_empty(defaultMean)){
                defaultMean <<- numeric(objective_fun$dim)
            }
            if(is_empty(population)){
                population <<- gen_random_population()
            }
            if(is_empty(lambda)){
                lambda <<- dim(population)[1]
            }
            if(is_empty(mu)){
                mu <<- floor(lambda/2)
            }
            if(is_empty(weights)){
                tmp <- log(mu+1) - log(1:mu)
                weights <<- tmp/sum(tmp)
            }
            if(is_empty(weightsPop)){
                tmp <- log(lambda+1) - log(1:lambda)
                weightsPop <<- tmp/sum(tmp)
            }
            if(is_empty(mueff)){
                mueff <<- sum(weights)^2/sum(weights^2)
            }
            if(is_empty(cc)){
                cc <<- mu/(mu+2)
            }
            if(is_empty(pathLength)){
                pathLength <<- 6
            }
            if(is_empty(cp)){
                cp <<- 1/sqrt(objective_fun$dim)
            }
            if(is_empty(Ft)){
                Ft <<- 1
            }
            if(is_empty(c_Ft)){
                c_Ft <<- 0
            }
            if(is_empty(pathRatio)){
                pathRatio <<- sqrt(pathLength)
            }
            if(is_empty(histSize)){
                histSize <<- ceiling(6+ceiling(3*sqrt(objective_fun$dim)))
            }
        },

        population_2_matrix = function(df){
            return(t(data.matrix(df[,!(names(df)=='fitness')])))
        },

        matrix_2_population = function(mat){
            fitness <- c()
            for(i in 1:dim(mat)[2]){
                fitness[i]<-objective_fun$evaluate(mat[,i])
            }
            return(data.frame(t(mat), fitness))
        },

        selection = function(df, offspring_num){
            df_sorted <- df[order(df['fitness'], decreasing=FALSE),]
            selected_points <- df_sorted[1:offspring_num,]
            return(selected_points)
        },

        # sampleFromHistory = function(history,historySample,lambda){
        # # ret <- c()
        # # for(i in 1:lambda)
        # #     # ret <- c(ret,sample(1:ncol(history[[historySample[i]]]), 1))
        # #     ret <- c(ret,sample(1:mu, 1))
        # ret <- sample(1:mu,lambda,T)
        # return(ret)
        # },

        run = function(){
            # default parameter init
            init_default_parameters()

            if(point_dim == 2){
                LOG_POPS <- TRUE
                first_pops <<- list(population) 
            }else{
                LOG_POPS <- FALSE
            }

            tol <- 10e-30
            # dynamic parameter init
            # steps       <- ringbuffer(size = (pathLength*objective_fun$dim))   
            dMean       <- array(0, dim=c(objective_fun$dim,histSize))
            # FtHistory   <- array(0, histSize)                                 
            pc       <- array(0, dim=c(objective_fun$dim,histSize))

            # history init
            histHead    <- 0
            history     <- list()

            # population <<- gen_random_population()
            population_mat <- population_2_matrix(population)
            best_point <- sel_best()

            oldMean         <- numeric(objective_fun$dim)
            newMean         <- defaultMean
  
            # Store population and selection means
            # print(population_mat)
            # print(weightsPop)
            popMean         <- drop(population_mat %*% weightsPop)
            muMean          <- newMean

            ## Matrices for creating diffs
            diffs     <- matrix(0, objective_fun$dim, lambda)
            x1sample  <- numeric(lambda)
            x2sample  <- numeric(lambda)

            # chiN      <- (sqrt(2)*gamma((objective_fun$dim+1)/2)/gamma(objective_fun$dim/2))
            histNorm  <- 1/sqrt(2)

            mean_time <- 0
            iterations  <<- 0
            times_vec <- c()
            while(iterations < max_iter && objective_fun$evaluate(best_point) > tolerance){
                start_time <- Sys.time()
                if(LOG_POPS && iterations <20){
                    first_pops <<- list.append(first_pops, population)
                }

                iterations  <<- iterations + 1L
                histHead  <- (histHead %% histSize) + 1

                selectedPoints_df <- selection(population, offspring_num=mu)
                selectedPoints_mat <- population_2_matrix(selectedPoints_df)

                # Save selected population in the history buffer
                history[[histHead]] <- array(0,dim=c(objective_fun$dim,mu))
                history[[histHead]] <- selectedPoints_mat * histNorm/Ft

                ## Calculate weighted mean of selected points
                oldMean <- newMean
                newMean <- drop(selectedPoints_mat %*% weights)

                ## Write to buffers
                muMean <- newMean
                dMean[,histHead] <- (muMean - popMean) / Ft

                step <- (newMean - oldMean) / Ft
                # ## Update Ft
                # FtHistory[histHead] = Ft

                if(histHead==1){
                    pc[,histHead] = (1 - cp)* numeric(objective_fun$dim)/sqrt(objective_fun$dim) + sqrt(mu * cp * (2-cp))* step
                # pc[,histHead] = (1 - cp)* rep(0.0, objective_fun$dim)/sqrt(objective_fun$dim) + sqrt(mu * cp * (2-cp))* step
                }else{
                pc[,histHead] = (1 - cp)* pc[,histHead-1] + sqrt(mu * cp * (2-cp))* step
                }
                ## Sample from history with uniform distribution
                limit <- min(iterations, histSize)
                historySample <- sample(1:limit,lambda, T)
                historySample2 <- sample(1:limit,lambda, T)

                # x1sample <- sampleFromHistory(history,historySample,lambda)
                # x2sample <- sampleFromHistory(history,historySample,lambda)
                x1sample <- sample(1:mu, lambda, T)
                x2sample <- sample(1:mu, lambda, T)

                ## Make diffs
                for (i in 1:lambda) {
                    x1 <- history[[historySample[i]]][,x1sample[i]]
                    x2 <- history[[historySample[i]]][,x2sample[i]]

                    diffs[,i] <- sqrt(cc)*( (x1 - x2) + rnorm(1)*dMean[,historySample[i]] ) + sqrt(1-cc) * rnorm(1)*pc[,historySample2[i]]
                }

                ## New population
                # population_mat <- newMean + Ft * diffs + tol*rnorm(diffs)/chiN
                population_mat <- newMean + Ft * diffs
                # population_mat <- deleteInfsNaNs(population_mat)

                population <<- matrix_2_population(population_mat)
                best_point <- sel_best()
                popMean <- drop(population_mat %*% weightsPop)
                times_vec[iterations] <- (Sys.time() - start_time)
                # mean_time <- times_vec[iterations]
            }
        mean_time <- sum(times_vec)/iterations
        mean_time <- as.numeric(mean_time, units="secs")
        return(new('Result', best_point=best_point, end_reason='max_iter',mean_iteration_time=mean_time, iterations=iterations, times_list=times_vec))        
    }
    )
) 