library(pracma)

P <- read.csv("C:\\Users\\Tata\\Desktop\\OptimizationAlgorithms\\R_shallow\\temp.csv", header = FALSE)
population <- as.matrix(P)

sum_of_squares<-function(point){
  sum <- 0.0
  for(p in point)
  {
    sum <- sum + p^2
  }
  return(sum)
}

# static parameters init
counteval <- 200
population_size <- dim(population)[1]
point_dim <- dim(population)[2]
m <- runif(point_dim)
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
B <- eye(point_dim)                       
D <- ones(point_dim , 1 ) 
# C <- B %*% diag(D^2) %*% t(B)           
# invsqrtC <- B %*% diag(D^(-1)) %*% t(B)   
C <- eye(point_dim)
invsqrtC <- eye(point_dim)

eigeneval <- 0                    
chiN <- point_dim^0.5*(1-1/(4*point_dim)+1/(21*point_dim^2))

t <- 0
while(t < 200){
  t <- t+1
  generated_pop <- m + sigma * MASS::mvrnorm(population_size, mu = numeric(point_dim), Sigma = C)

  fitnesses <- c()
  for (i in 1:dim(generated_pop)[1]){
      point <- generated_pop[i,]
      fitness <- sum_of_squares(point)
      fitnesses <- append(fitnesses, fitness)
  }

  generated_pop_sorted <- generated_pop[order(fitnesses, decreasing=FALSE),]
  new_m <- t(generated_pop_sorted)[,1:mu] %*% weights
  ps <- (1-cs)*ps + sqrt(cs*(2-cs)*mueff) * invsqrtC %*% (new_m-m) / sigma
  hsig <- norm(ps)/sqrt(1-(1-cs)^(2*counteval/lambda))/chiN < 1.4 + 2/(point_dim+1)
  pc <- (1-cc)*pc + hsig * sqrt(cc*(2-cc)*mueff) * (new_m-m) / sigma
  artmp <- (1/sigma) * (t(generated_pop_sorted)[,1:mu] - matrix(rep(m,mu), point_dim, mu))
  C <- (1-c1-cmu) * C + c1*(pc%*%t(pc) + (1-hsig)*cc*(2-cc)*C) + cmu * artmp %*% diag(weights) %*% t(artmp)
  sigma <- sigma * exp((cs/damps)*(norm(ps)/chiN - 1))
 
  print(sum_of_squares(generated_pop_sorted[1,]))
    
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
  m <- c(new_m)
}