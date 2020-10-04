library(pracma)

# this language sucks so much ass ehhhhhhhhhhhhh
P <- read.csv("C:\\Users\\Lenovo\\Desktop\\Studia\\INZYNIERKA\\OptimizationAlgorithms\\R_shallow\\data.csv", header = FALSE)
population <- as.matrix(P)


# static parameters init
population_size <- dim(population)[1]
point_dim <- dim(population)[2]
m <- mean(population)
sigma <- 0.3 
lambda <- 4 + floor(3*log(point_dim))
mu <- lambda/2
weights <- log(mu+1/2)-log(1:mu)
mu <- floor(mu)
weights <- weights/sum(weights)
mueff <- sum(weights)^2/sum(weights^2)
cc <-  (4+mueff/point_dim) / (point_dim+4 + 2*mueff/point_dim)
cs <-  (mueff+2) / (point_dim+mueff+5)
c1 <- 2 / ((point_dim+1.3)^2+mueff)
cmu <- min(1-c1, 2 * (mueff-2+1/mueff) / ((point_dim+2)^2+mueff))
damps <- 1 + 2*max(0, sqrt((mueff-1)/(point_dim+1))-1) + cs

# dynamic parameters init
pc <- numeric(point_dim)
ps <- numeric(point_dim)
B <- eye(point_dim , point_dim )                       
D <- ones(point_dim , 1 )                      
C <- B %*% diag(D^2) %*% t(B)           
invsqrtC <- B %*% diag(D^(-1)) %*% t(B)    
eigeneval <- 0                    
chiN <- point_dim^0.5*(1-1/(4*point_dim)+1/(21*point_dim^2))


sel_best<-function(population){
  val_array <- c()
  for(p in 1:mi){
    val_array<-append(val_array, sum_of_squares(population[p,]))
  }
  min_index <- which.min(val_array)
  return(population[min_index,])
}

sum_of_squares<-function(point){
  sum <- 0.0
  for(p in point)
  {
    sum <- sum + p^2
  }
  return(sum)
}


t <- 0
while(t != 200)
{
  for (k in 1:lambda){
    arx(:,k) <- m + sigma * B * (D* randn(point_dim,1)) 
    arfitness(k) <- feval(strfitnessfct, arx(:,k)); % objective function call
    counteval <- counteval + 1
  }

  d <- MASS::mvrnorm(population_size, mu = numeric(point_dim), Sigma = C)
  q <- vector()
  for(di in d){
    qi <- sum_of_squares(m+sigma*di)
    q <- append(q, qi)
  }
  d <- d[order(q, decreasing=FALSE)] 
  delta <- 1/mi * rowSums(d[0:mi,])
  m_next <- m + sigma*delta
  C_fact <- 
  p_sgm_next <- (1 - c_sgm)*p_sgm +  

}

