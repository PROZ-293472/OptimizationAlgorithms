library(pracma)
library(comprehenr)
source("Classes.R")

is_empty <- function(x) return(length(x) ==0 )

DES <- setRefClass(
    "DES",
    contains = "Algorithm",
    fields = list(
        lambda = "numeric",
        mu = "numeric",
        weights = "numeric",
        mu_w = "numeric",
        cc = "numeric",
        path_len = "numeric",
        cp = "numeric",
        c_Ft = "numeric",
        path_ratio = "numeric",
        hist_size = "numeric",
        Ft_scale = "numeric"
    ),
    methods = list(
        init_default_parameters = function(){
            if(is_empty(population)){
                population <<- gen_random_population()
            }
            if(is_empty(lambda)){
                lambda <<- 4*objective_fun$dim
            }
            if(is_empty(mu)){
                mu <<- floor(lambda/2)
            }
            if(is_empty(weights)){
                tmp <- log(mu+1) - log(1:mu))
                weights <<- tmp/sum(tmp)
            }
            if(is_empty(mu_w)){
                mu_w <<- sum(weights)^2/sum(weights^2)
            }
            if(is_empty(cc)){
                cc <<- mu/(mu+2)
            }
            if(is_empty(path_len)){
                path_len <<- 6
            }
            if(is_empty(cp)){
                cp <<- 1/sqrt(objective_fun$dim)
            }
            if(is_empty(c_Ft)){
                c_Ft <<- 0
            }
            if(is_empty(path_ratio)){
                path_ratio <<- sqrt(path_len)
            }
            if(is_empty(hist_size)){
                hist_size <<- ceiling(6+ceiling(3*sqrt(objective_fun$dim))
            }
            if(is_empty(Ft_scale)){
                Ft_scale <<- ((mu_w+2)/(objective_fun$dim+mu_w+3))/(1 + 2*max(0, sqrt((mu_w-1)/(objective_fun$dim+1))-1) + (mu_w+2)/(objective_fun$dim+mu_w+3))
            }
        },
        run = function(){
            selection <- rep(0, mu)
            selectedPoints <- matrix(0, nrow=objective_fun$dim, ncol=mu)
            fitness <- 

        } 