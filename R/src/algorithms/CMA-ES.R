# this language sucks so much ass ehhhhhhhhhhhhh
P <- read.csv("C:\\Users\\Lenovo\\Desktop\\Studia\\INZYNIERKA\\OptimizationAlgorithms\\R\\src\\data.csv", header = FALSE)
population <- as.matrix(P)

population_size <- dim(population)[1]
point_dim <- dim(population)[2]
C <-  diag(point_dim)
p_c <- numeric(point_dim)
p_sgm <- numeric(point_dim)


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
m <- mean(population)
sigma <- 1
mi <- population_size/2
while(t != 200)
{
  d <- MASS::mvrnorm(population_size, mu = numeric(point_dim), Sigma = C)
  q <- vector()
  for(di in d){
    qi <- sum_of_squares(m+sigma*di)
    append(q, qi)
  }
  d <- d[order(q, decreasing=FALSE)] 
  delta <- 1/mi * rowSums(d[0:mi,])
  m_next <- m + sigma*delta
  C_fact <- 
  p_sgm_next <- (1 - c_sgm)*p_sgm + 

}